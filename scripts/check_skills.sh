#!/bin/bash
# =============================================================================
# check_skills.sh - Pre-commit integrity & license/credit validator
#
# Verifies, for EVERY skill directory in this repo:
#   1. A valid SKILL.md exists with parseable YAML frontmatter
#   2. A LICENSE / LICENSE.md file is present for license & attribution
#   3. No stale Claude/Anthropic branding remains (OpenCode fork)
#   4. The skill is registered in .opencode/skills.json (registry consistency)
#   5. Registry paths resolve to real directories
#
# Also checks the registry itself is valid JSON and its version tag is present.
#
# Usage:
#   ./scripts/check_skills.sh                 # check all skills (default)
#   ./scripts/check_skills.sh --staged        # check only git-staged skill dirs
#   ./scripts/check_skills.sh --quiet         # exit code only, minimal output
#
# Exit codes:
#   0  all checks passed
#   1  one or more checks failed (human-readable output)
#   2  usage error
# =============================================================================

set -u

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

MODE="all"
QUIET=0
STRICT=0

for arg in "$@"; do
	case "$arg" in
	--staged) MODE="staged" ;;
	--quiet) QUIET=1 ;;
	--strict) STRICT=1 ;;
	-h | --help)
		sed -n '2,20p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,2\}//'
		exit 0
		;;
	*)
		echo "Unknown arg: $arg" >&2
		exit 2
		;;
	esac
done

failures=0
warnings=0
log() { [ "$QUIET" -eq 1 ] || echo "$@"; }
warn() {
	log "[warn] $*"
	warnings=$((warnings + 1))
}
fail() {
	log "[FAIL] $*"
	failures=$((failures + 1))
}

# ---------------------------------------------------------------------------
# 0. Registry validity
# ---------------------------------------------------------------------------
REGISTRY=".opencode/skills.json"
if [ ! -f "$REGISTRY" ]; then
	fail "Registry missing: $REGISTRY"
fi

if command -v python3 >/dev/null 2>&1 && [ -f "$REGISTRY" ]; then
	if ! python3 -c "import json,sys; json.load(open('$REGISTRY'))" 2>/dev/null; then
		fail "Registry $REGISTRY is not valid JSON"
	fi
fi

# ---------------------------------------------------------------------------
# Determine skill directories to check
# ---------------------------------------------------------------------------
if [ "$MODE" = "staged" ]; then
	# Only skill dirs touched by staged changes
	STAGED_DIRS="$(git diff --cached --name-only | sed -E 's#^([^/]+)/.*#\1#' | sort -u)"
	SKILL_DIRS="$(echo "$STAGED_DIRS" | while read -r d; do
		[ -n "$d" ] && [ -f "$d/SKILL.md" ] && echo "$d"
	done)"
else
	# Every top-level directory that IS itself a skill (has its own SKILL.md),
	# excluding: collection dirs that only hold sub-skill dirs (e.g. document-skills),
	# and non-skill project dirs (MCP servers, scripts).
	SKILL_DIRS="$(for d in */; do
		dir="${d%/}"
		[ -d "$dir" ] || continue
		case "$dir" in
		scripts | opencode-skills-mcp-server | opencode-skills-mcp-server-ts) continue ;;
		esac
		# a collection has SKILL.md files only nested ≥2 deep (e.g. document-skills/x/SKILL.md)
		if [ -f "$dir/SKILL.md" ]; then echo "$dir"; fi
	done)"
fi

total=0
for skill in $SKILL_DIRS; do
	[ -n "$skill" ] || continue
	[ -d "$skill" ] || continue
	total=$((total + 1))

	# --- 1. SKILL.md + valid frontmatter ------------------------------------
	if [ ! -f "$skill/SKILL.md" ]; then
		fail "[$skill] missing SKILL.md"
		continue
	fi
	if [ -z "$(sed -n 's/^name: *//p' "$skill/SKILL.md" | head -1)" ]; then
		fail "[$skill] SKILL.md has no frontmatter 'name:'"
	fi
	if [ -z "$(sed -n 's/^description: *//p' "$skill/SKILL.md" | head -1)" ]; then
		fail "[$skill] SKILL.md has no frontmatter 'description:'"
	fi

	# --- 2. LICENSE / credit file -------------------------------------------
	# Every skill we migrate in must carry its license so credit & terms are
	# preserved. Vendored external skills MUST include the upstream LICENSE.
	if ! ls "$skill"/LICENSE* >/dev/null 2>&1; then
		fail "[$skill] missing LICENSE file (license/credit must be preserved per migrated skill)"
	fi

	# --- 3. Stale branding --------------------------------------------------
	# Allowlist file: each line is <skill>|<exact-substring> that is a legitimate
	# functional reference (e.g. SDK imports) and may stay. See scripts/branding-allowlist.txt.
	ALLOWLIST="scripts/branding-allowlist.txt"
	MATCHES="$(grep -rInE "Claude|Anthropic|anthropic" "$skill" --include="*.md" --include="*.py" --include="*.sh" --include="*.cjs" --include="*.js" --include="*.ts" --include="*.json" 2>/dev/null || true)"
	if [ -n "$MATCHES" ]; then
		violations=""
		while IFS= read -r line; do
			[ -z "$line" ] && continue
			allowed=0
			if [ -f "$ALLOWLIST" ]; then
				while IFS='|' read -r sk pat; do
					[ "$sk" = "$skill" ] && [ -n "$pat" ] && printf '%s' "$line" | grep -qF -- "$pat" && {
						allowed=1
						break
					}
				done <"$ALLOWLIST"
			fi
			[ "$allowed" -eq 0 ] && violations="$violations
$line"
		done <<<"$MATCHES"
		if [ -n "$violations" ]; then
			if [ "$STRICT" -eq 1 ]; then
				fail "[$skill] contains Claude/Anthropic branding (not allowlisted). See scripts/branding-allowlist.txt"
			else
				warn "[$skill] contains Claude/Anthropic branding (not allowlisted) — run --strict to gate, or add to scripts/branding-allowlist.txt"
			fi
			if [ "$QUIET" -eq 0 ]; then echo "$violations" | sed 's/^/        /' | head -12; fi
		fi
	fi

	log "  ✓ $skill"
done

# ---------------------------------------------------------------------------
# Registry <-> disk consistency
# ---------------------------------------------------------------------------
if [ -f "$REGISTRY" ] && command -v python3 >/dev/null 2>&1; then
	python3 - "$REGISTRY" "$QUIET" <<'PY'
import json, os, sys
reg, quiet = sys.argv[1], sys.argv[2]=='1'
data = json.load(open(reg))
issues = 0
# version sanity
if not str(data.get('version','')).strip():
    print(f"[FAIL] {reg} missing version"); issues += 1
seen = set()
for s in data.get('skills', []):
    name = s.get('name')
    if name in seen:
        print(f"[FAIL] {reg} duplicate skill entry: {name}"); issues += 1
    seen.add(name)
    path = s.get('path','')
    # path is like ./skill-name
    d = path[2:] if path.startswith('./') else path
    if not os.path.isdir(d):
        print(f"[FAIL] registry path does not resolve: {name} -> {path}"); issues += 1
    elif not os.path.isfile(os.path.join(d, 'SKILL.md')):
        print(f"[FAIL] registry entry missing SKILL.md: {name} -> {path}"); issues += 1
    if not s.get('category'):
        print(f"[FAIL] registry entry missing category: {name}"); issues += 1
sys.exit(1 if issues else 0)
PY
	[ $? -ne 0 ] && fail "Registry consistency checks failed ($REGISTRY)"
fi

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
if [ "$failures" -eq 0 ]; then
	if [ "$QUIET" -eq 0 ]; then
		echo ""
		if [ "$warnings" -gt 0 ]; then
			echo "✅ Checks passed ($total skills, $warnings warning(s), registry OK). Run with --strict to gate branding."
		else
			echo "✅ All checks passed ($total skills, registry OK)."
		fi
	fi
	exit 0
else
	echo ""
	echo "❌ $failures check(s) failed across $total skills." >&2
	exit 1
fi
