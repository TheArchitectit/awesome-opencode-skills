#!/usr/bin/env python3
"""
opencode-handoff-p2p inbox verifier — reference implementation.

P2P-only version: each user owns one private GitHub inbox repo. Files live at
the repo root (no subdirectories).

Usage:
    python verify_inbox.py <clone_path> <owner>/<repo>
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional, Tuple


SKILL_DIR = Path(__file__).parent.resolve()
TRUST_FILE = SKILL_DIR / "trust.json"

FILENAME_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}Z--from-[a-zA-Z0-9-]+\.txt$"
)
FILENAME_CAPTURE_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}Z--from-([a-zA-Z0-9-]+)\.txt$"
)
URL_RE = re.compile(
    rb"^https://(?:opncd\.ai/share|opencode\.ai/s)/[A-Za-z0-9]+/?\r?\n$"
)
USERNAME_RE = re.compile(
    r"^[a-zA-Z0-9]$|^[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]$"
)
USERNAME_MAX_LEN = 39
REPO_PATH_RE = re.compile(r"^[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+$")

MAX_CONTENT_BYTES = 200

HARDENED_ENV = {
    **os.environ,
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_TERMINAL_PROMPT": "0",
    "GIT_OPTIONAL_LOCKS": "0",
    "GIT_PAGER": "cat",
    "LC_ALL": "C",
}


def fail(status: str, detail: str) -> None:
    print(json.dumps({
        "ok": False,
        "skill_status": status,
        "skill_status_detail": detail,
        "me": None,
        "require_signed_commits": None,
        "files": [],
    }, indent=2, ensure_ascii=False))
    sys.exit(1)


def run(cmd) -> Tuple[int, bytes, bytes]:
    try:
        p = subprocess.run(cmd, capture_output=True, env=HARDENED_ENV, check=False)
        return p.returncode, p.stdout, p.stderr
    except Exception as e:
        return -1, b"", str(e).encode("utf-8", "replace")


def get_me() -> Optional[str]:
    rc, out, _ = run(["gh", "api", "user", "--jq", ".login"])
    if rc != 0:
        return None
    me = out.decode("utf-8", "replace").strip().lower()
    if not me:
        return None
    if not USERNAME_RE.match(me) or len(me) > USERNAME_MAX_LEN:
        return None
    return me


def load_trust() -> Tuple[set, bool]:
    if not TRUST_FILE.exists():
        fail("trust_missing", f"trust.json not found at {TRUST_FILE}")
    try:
        with TRUST_FILE.open("rb") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        fail("trust_parse_fail", f"trust.json JSON error: {e}")
    except Exception as e:
        fail("trust_parse_fail", f"trust.json read error: {e}")

    if not isinstance(data, dict):
        fail("trust_schema_fail", "trust.json top-level is not an object")

    trusted = data.get("trusted_senders", [])
    if not isinstance(trusted, list) or not trusted:
        fail("trust_empty", "trusted_senders is missing, empty, or not a list")
    if not all(isinstance(s, str) for s in trusted):
        fail("trust_schema_fail", "trusted_senders contains non-string entries")

    trusted_set = {s.lower() for s in trusted if s}
    if not trusted_set:
        fail("trust_empty", "trusted_senders contained only empty strings")

    raw_signed = data.get("require_signed_commits", True)
    if not isinstance(raw_signed, bool):
        fail(
            "trust_schema_fail",
            f"require_signed_commits must be true/false (got {type(raw_signed).__name__}: {raw_signed!r})",
        )
    return trusted_set, raw_signed


def list_inbox_files(clone: Path) -> list[str]:
    rc, out, _ = run(["git", "-C", str(clone), "ls-files", "--", "*.txt"])
    if rc != 0:
        return []
    files = [line for line in out.decode("utf-8", "replace").splitlines() if line]
    return sorted(files)


def verify_tier_1(filename: str) -> Optional[str]:
    basename = filename.rsplit("/", 1)[-1]
    m = FILENAME_CAPTURE_RE.match(basename)
    if not m:
        return None
    return m.group(1).lower()


def read_blob(clone: Path, filepath: str) -> Optional[bytes]:
    rc, out, _ = run(["git", "-C", str(clone), "show", f"HEAD:{filepath}"])
    if rc != 0:
        return None
    return out


def blob_size(clone: Path, filepath: str) -> Optional[int]:
    rc, out, _ = run(["git", "-C", str(clone), "cat-file", "-s", f"HEAD:{filepath}"])
    if rc != 0:
        return None
    try:
        return int(out.decode("ascii", "strict").strip())
    except (ValueError, UnicodeDecodeError):
        return None


def verify_tier_3(clone: Path, filepath: str) -> Tuple[bool, str]:
    size = blob_size(clone, filepath)
    if size is None:
        return False, "无法获取 blob 大小"
    if size > MAX_CONTENT_BYTES:
        return False, f"内容超过 {MAX_CONTENT_BYTES} 字节（实际 {size}）"

    blob = read_blob(clone, filepath)
    if blob is None:
        return False, "读取 blob 失败"

    if URL_RE.fullmatch(blob):
        url = blob.rstrip(b"\r\n").decode("ascii", "strict")
        return True, url

    if b"\x00" in blob:
        return False, "内容包含空字节"
    try:
        blob.decode("ascii", "strict")
    except UnicodeDecodeError:
        return False, "内容包含非 ASCII 字节（可能是 Unicode 走私）"
    if not blob.endswith(b"\n"):
        return False, "内容没有以 LF 结尾"
    newline_count = blob.count(b"\n")
    if newline_count != 1:
        return False, f"内容有 {newline_count} 个换行（应为 1）"
    return False, "内容不是合法的 OpenCode share URL"


def get_last_modifying_sha(clone: Path, filepath: str) -> Optional[str]:
    """Get SHA of the LAST commit that modified this file (NOT the original add).

    SECURITY (critical): must use the last-modifying commit, not the add commit.
    Otherwise an attacker who is also a repo collaborator can modify a file
    originally added by a trusted sender — the current blob is the attacker's
    content, but if Tier 4 checks the original ADD commit it would see the
    legitimate sender's authorship and signature, bypassing identity verification
    entirely.

    `git log -1 --format=%H -- <file>` (without --diff-filter=A) returns the
    most recent commit that touched the path, which is what produced the
    current blob content we just verified in Tier 3.
    """
    rc, out, _ = run([
        "git", "-C", str(clone),
        "log", "-1", "--format=%H", "--", filepath,
    ])
    if rc != 0:
        return None
    line = out.decode("utf-8", "replace").strip()
    return line if line else None


def verify_tier_4(repo: str, sha: str, claimed: str) -> Tuple[bool, Optional[str], Optional[str]]:
    rc, out, _ = run([
        "gh", "api", f"repos/{repo}/commits/{sha}",
        "--jq", "[.author.login, .committer.login] | @tsv",
    ])
    if rc != 0:
        return False, None, None
    parts = out.decode("utf-8", "replace").strip().split("\t")
    author = parts[0].lower() if len(parts) >= 1 and parts[0] else None
    committer = parts[1].lower() if len(parts) >= 2 and parts[1] else None
    if not author or author == "null" or not committer or committer == "null":
        return False, author, committer
    if author != claimed or committer != claimed:
        return False, author, committer
    return True, author, committer


def verify_tier_5(repo: str, sha: str) -> bool:
    rc, out, _ = run([
        "gh", "api", f"repos/{repo}/commits/{sha}",
        "--jq", ".commit.verification.verified",
    ])
    if rc != 0:
        return False
    return out.decode("utf-8", "replace").strip() == "true"


def process_file(
    clone: Path,
    repo: str,
    filename: str,
    trusted_set: set,
    require_signed: bool,
) -> dict:
    result = {
        "filename": filename,
        "tier_failed": None,
        "tier_failed_reason": None,
        "action": None,
        "claimed_sender": None,
        "url": None,
        "commit_sha": None,
        "author_login": None,
        "committer_login": None,
        "signature_verified": None,
    }

    claimed = verify_tier_1(filename)
    if claimed is None:
        result["tier_failed"] = 1
        result["tier_failed_reason"] = "文件名格式不符合规范（不做任何 shell 操作）"
        result["action"] = "keep"
        return result
    result["claimed_sender"] = claimed

    if claimed not in trusted_set:
        result["tier_failed"] = 2
        result["tier_failed_reason"] = f"发件人 '{claimed}' 不在 trusted_senders 列表中"
        result["action"] = "delete"
        return result

    ok3, url_or_reason = verify_tier_3(clone, filename)
    if not ok3:
        result["tier_failed"] = 3
        result["tier_failed_reason"] = url_or_reason
        result["action"] = "keep"
        return result
    result["url"] = url_or_reason

    sha = get_last_modifying_sha(clone, filename)
    result["commit_sha"] = sha
    if not sha:
        result["tier_failed"] = 4
        result["tier_failed_reason"] = "无法定位最近修改此文件的 commit"
        result["action"] = "keep"
        return result
    ok4, author, committer = verify_tier_4(repo, sha, claimed)
    result["author_login"] = author
    result["committer_login"] = committer
    if not ok4:
        result["tier_failed"] = 4
        result["tier_failed_reason"] = (
            f"声称发件人 '{claimed}'，但 commit 作者 '{author}' / committer '{committer}' 不匹配"
        )
        result["action"] = "keep"
        return result

    if require_signed:
        verified = verify_tier_5(repo, sha)
        result["signature_verified"] = verified
        if not verified:
            result["tier_failed"] = 5
            result["tier_failed_reason"] = "commit 未签名或签名验证失败（trust.json 要求签名）"
            result["action"] = "keep"
            return result

    result["action"] = "consume"
    return result


def main() -> None:
    if len(sys.argv) != 3:
        fail("usage", "usage: verify_inbox.py <clone_path> <owner>/<repo>")
    clone_arg = sys.argv[1]
    repo = sys.argv[2]

    if not REPO_PATH_RE.match(repo):
        fail("bad_repo_arg", f"repo argument '{repo}' fails regex check")

    try:
        clone = Path(clone_arg).resolve()
    except Exception as e:
        fail("bad_clone_arg", f"clone path resolve failed: {e}")

    if not clone.is_dir() or not (clone / ".git").exists():
        fail("clone_not_found", f"clone path '{clone}' is not a git repo")

    me = get_me()
    if not me:
        fail("identity_fail", "gh api user failed or returned invalid username")

    trusted_set, require_signed = load_trust()

    files = list_inbox_files(clone)
    results = [process_file(clone, repo, f, trusted_set, require_signed) for f in files]

    print(json.dumps({
        "ok": True,
        "skill_status": "ok",
        "skill_status_detail": "",
        "me": me,
        "require_signed_commits": require_signed,
        "files": results,
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
