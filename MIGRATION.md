# Migration from Claude Skills to OpenCode Skills

This repository was originally created for Claude Skills and has been migrated to support OpenCode.

## What Changed

### Branding Removal
1. **Removed all Claude/Anthropic branding**
   - Updated README.md to reference OpenCode instead of Claude
   - Updated CONTRIBUTING.md for OpenCode community
   - Removed Composio sponsorships and links
   - Updated all individual SKILL.md files to reference OpenCode

2. **Replaced Anthropic brand guidelines**
   - Updated `brand-guidelines/SKILL.md` with OpenCode branding
   - Updated color palette to match OpenCode theme
   - Updated typography recommendations (monospace for code)

3. **Removed Claude-specific files**
   - Deleted `.claude-plugin/marketplace.json` (Claude marketplace manifest)

### OpenCode-Specific Enhancements
1. **Added OpenCode tooling**
   - Created `scripts/install_opencode_skills.sh` - Installation helper for skills
   - Created `OPENCODE_SKILLS.md` - Skills index and usage guide
   - Created `.opencode/skills.json` - Skills metadata for OpenCode

2. **Updated skill installation paths**
   - Changed from `~/.config/claude-code/skills/` to `~/.config/opencode/skill/`
   - Added project-local installation to `.opencode/skill/`
   - Maintained backward compatibility with `.claude/skills/`

3. **Updated documentation**
   - All references to "Claude" → "OpenCode"
   - All references to "Claude.ai" → "OpenCode"
   - All references to "Claude Code" → "OpenCode"
   - Removed API usage section (OpenCode doesn't have skills API)

## Installation

### Quick Install

```bash
# Global installation (recommended)
./scripts/install_opencode_skills.sh --global

# Project-local installation
./scripts/install_opencode_skills.sh --project
```

### Individual Skills

```bash
# Install specific skill to global
./scripts/install_opencode_skills.sh --global brand-guidelines

# Install specific skill to project
./scripts/install_opencode_skills.sh --project brand-guidelines
```

## Compatibility

### Skill Format
Skills maintain the same SKILL.md format with YAML frontmatter:
- `name` (required) - Skill identifier
- `description` (required) - What the skill does
- `license` (optional) - License information

### Skill Discovery
OpenCode automatically discovers skills from:
- **Global**: `~/.config/opencode/skill/*/SKILL.md`
- **Project**: `.opencode/skill/*/SKILL.md`
- **Backward Compatible**: `.claude/skills/*/SKILL.md`

### Permissions
OpenCode supports skill permissions via `opencode.json`:

```json
{
  "permission": {
    "skill": {
      "*": "allow"
    }
  }
}
```

## Testing

### Validation
All skills have been validated to ensure:
- Proper YAML frontmatter format
- Correct naming convention (lowercase-hyphens)
- Description length within limits (1-1024 characters)
- No invalid characters in descriptions

### Load Testing
To test skill loading:

1. Install skills:
   ```bash
   ./scripts/install_opencode_skills.sh --global
   ```

2. Start OpenCode:
   ```bash
   opencode
   ```

3. Verify skills are discovered:
   - Check that skills appear in the skill list
   - Try loading a skill to verify it works correctly

## Credits

Originally based on awesome-claude-skills repository.
Migrated to OpenCode by TheArchitectit team.

## Resources

- [OpenCode Skills Documentation](https://opencode.ai/docs/skills/)
- [OpenCode GitHub Repository](https://github.com/sst/opencode)
- [OpenCode Discord Community](https://opencode.ai/discord)
- [OpenCode Configuration](https://opencode.ai/docs/config/)
