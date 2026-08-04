#!/bin/bash
# install_check_hook.sh - Install the skills integrity pre-commit hook
#
# Installs scripts/check_skills.sh as a git pre-commit hook so every commit
# validates: LICENSE presence per skill, valid SKILL.md frontmatter, registry
# consistency, and (in --strict) stale-branding gating.
#
# Usage:   ./scripts/install_check_hook.sh
# Uninstall: ./scripts/install_check_hook.sh --remove

set -e
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOOK="$ROOT/.git/hooks/pre-commit"
SRC="$ROOT/scripts/check_skills.sh"

if [ "${1:-}" = "--remove" ]; then
  if [ -f "$HOOK" ] && grep -q "check_skills.sh" "$HOOK"; then
    rm -f "$HOOK"
    echo "🗑️  Removed pre-commit hook."
  else
    echo "No installed check_skills hook found."
  fi
  exit 0
fi

if [ ! -f "$SRC" ]; then
  echo "❌ $SRC not found." >&2
  exit 1
fi

mkdir -p "$(dirname "$HOOK")"
cat > "$HOOK" <<'EOF'
#!/bin/bash
# Pre-commit hook: run skills integrity/license/credit check on staged skills
ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"
if [ -n "$ROOT" ] && [ -f "$ROOT/scripts/check_skills.sh" ]; then
  echo "🔍 Running skills integrity check (license/credit gate)..."
  "$ROOT/scripts/check_skills.sh" --staged || {
    echo ""
    echo "❌ Pre-commit skills check failed. Fix the issues above, or run:"
    echo "     scripts/check_skills.sh --staged   # see details"
    exit 1
  }
fi
exit 0
EOF
chmod +x "$HOOK"
echo "✅ Installed pre-commit hook -> $HOOK"
echo "   (runs scripts/check_skills.sh --staged on every commit)"
