#!/bin/bash
# Install OpenCode Skills
# Usage: ./scripts/install_opencode_skills.sh [--global|--project] [skill-name]

set -e

INSTALL_MODE="global"
SKILL_NAME=""

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --global)
      INSTALL_MODE="global"
      shift
      ;;
    --project)
      INSTALL_MODE="project"
      shift
      ;;
    *)
      SKILL_NAME="$1"
      shift
      ;;
  esac
done

# Determine installation directory
if [ "$INSTALL_MODE" = "global" ]; then
  INSTALL_DIR="$HOME/.config/opencode/skill"
  echo "📦 Installing to global OpenCode skills directory: $INSTALL_DIR"
else
  INSTALL_DIR=".opencode/skill"
  echo "📦 Installing to project-local OpenCode skills directory: $INSTALL_DIR"
fi

# Create directory if needed
mkdir -p "$INSTALL_DIR"

# Install specific skill or all skills
if [ -n "$SKILL_NAME" ]; then
  if [ ! -d "$SKILL_NAME" ]; then
    echo "❌ Error: Skill directory '$SKILL_NAME' not found"
    exit 1
  fi
  echo "📁 Copying skill: $SKILL_NAME"
  cp -r "$SKILL_NAME" "$INSTALL_DIR/"
  echo "✅ Installed '$SKILL_NAME' to $INSTALL_DIR"
else
  echo "📁 Installing all skills..."
  for skill_dir in */; do
    if [ -f "${skill_dir}SKILL.md" ]; then
      echo "📁 Copying ${skill_dir%/}"
      cp -r "$skill_dir" "$INSTALL_DIR/"
    fi
  done
  echo "✅ Installed all skills to $INSTALL_DIR"
fi

echo ""
echo "🚀 Next steps:"
if [ "$INSTALL_MODE" = "global" ]; then
  echo "1. Start OpenCode: opencode"
else
  echo "1. Start OpenCode in this directory: opencode"
fi
echo "2. Skills will be automatically discovered"
