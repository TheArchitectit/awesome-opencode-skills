# OpenCode Skills Index

This document provides an index of all available OpenCode skills in this repository.

## Installation

### Quick Install (All Skills)

```bash
# Global installation (recommended)
./scripts/install_opencode_skills.sh --global

# Project-local installation
./scripts/install_opencode_skills.sh --project
```

### Install Individual Skill

```bash
# Global installation
./scripts/install_opencode_skills.sh --global skill-name

# Project-local installation
./scripts/install_opencode_skills.sh --project skill-name
```

## Skill Categories

### Document Processing
- `document-skills/docx` - Word document creation and editing
- `document-skills/pdf` - PDF manipulation and form filling
- `document-skills/pptx` - PowerPoint presentation creation
- `document-skills/xlsx` - Excel spreadsheet operations

### Development Tools
- `artifacts-builder` - Build HTML artifacts with React, Tailwind, shadcn/ui
- `changelog-generator` - Generate changelogs from git commits
- `developer-growth-analysis` - Analyze coding patterns and growth
- `mcp-builder` - Create MCP servers for external API integration
- `skill-creator` - Guide for creating new skills
- `webapp-testing` - Test web apps with Playwright

### Business & Marketing
- `brand-guidelines` - Apply OpenCode branding to artifacts
- `competitive-ads-extractor` - Analyze competitor advertisements
- `domain-name-brainstormer` - Generate domain name ideas
- `internal-comms` - Write internal communications
- `lead-research-assistant` - Research and qualify leads

### Communication & Writing
- `content-research-writer` - Research and write content
- `meeting-insights-analyzer` - Analyze meeting transcripts

### Creative & Media
- `canvas-design` - Create visual art and designs
- `image-enhancer` - Enhance image quality
- `slack-gif-creator` - Create animated GIFs
- `theme-factory` - Apply professional themes to artifacts
- `video-downloader` - Download videos from platforms

### Productivity & Organization
- `file-organizer` - Organize files and folders
- `invoice-organizer` - Organize invoices for tax prep
- `raffle-winner-picker` - Randomly select winners

## Configuration

Skills are automatically discovered from:
- Global: `~/.config/opencode/skill/*/SKILL.md`
- Project: `.opencode/skill/*/SKILL.md`
- Backward compatible: `.claude/skills/*/SKILL.md`

You can control skill access permissions in your `opencode.json`:

```json
{
  "permission": {
    "skill": {
      "*": "allow"
    }
  }
}
```

## Troubleshooting

### Skills Not Appearing

**Problem**: Skills don't appear in OpenCode's skill list

**Solutions**:

1. **Check Installation Directory**:
   ```bash
   ls -la ~/.config/opencode/skill/
   # Should list skill folders with SKILL.md files
   ```

2. **Verify SKILL.md Format**:
   - Each skill must have `SKILL.md` at root of skill folder
   - File must include YAML frontmatter with `name` and `description`
   - Run validation: `python3 skill-creator/scripts/quick_validate.py <skill-path>`

3. **Check Permissions**:
   ```bash
   # Verify OpenCode has read permissions
   ls -la ~/.config/opencode/skill/
   chmod -R +r ~/.config/opencode/skill/
   ```

4. **Restart OpenCode**:
   - OpenCode loads skills on startup
   - Exit and restart after installing new skills

### Skill Loading Errors

**Problem**: Error when skill loads or executes

**Solutions**:

1. **Check Skill Syntax**:
   - Validate YAML frontmatter format
   - Ensure no special characters in description
   - Description length: 1-1024 characters

2. **Review Dependencies**:
   - Some skills require external tools (Python, Node.js, pandoc, etc.)
   - Install missing dependencies
   - Check skill's SKILL.md for prerequisites section

3. **Check File Paths**:
   - Bundled resources (scripts/, references/, assets/) must be in skill directory
   - Relative paths must be correct
   - No symlinks outside skill directory

### Installation Script Issues

**Problem**: Installation script fails

**Solutions**:

1. **Make Script Executable**:
   ```bash
   chmod +x scripts/install_opencode_skills.sh
   ```

2. **Check Script Path**:
   ```bash
   # Run from repository root
   cd /path/to/awesome-opencode-skills
   ./scripts/install_opencode_skills.sh --global
   ```

3. **Verify Python Installed**:
   ```bash
   python3 --version
   # Should be Python 3.7+
   ```

4. **Check Available Space**:
   ```bash
   df -h ~/.config/opencode/skill/
   # Ensure sufficient disk space
   ```

### Multiple Skill Versions

**Problem**: Same skill installed in multiple locations

**Solution**:

OpenCode uses this priority order:
1. `.opencode/skill/` (project-local, highest priority)
2. `~/.config/opencode/skill/` (global)
3. `.claude/skills/` (backward compatible)

If you have duplicates, remove from lower-priority locations:
```bash
# Remove project-local duplicate
rm -rf .opencode/skill/duplicate-skill

# Keep global version
ls ~/.config/opencode/skill/
```

### Skill Not Triggering

**Problem**: Skill should load but doesn't activate

**Solutions**:

1. **Check Description Relevance**:
   - Skill's `description` in YAML frontmatter determines when it loads
   - Update description to be more specific about use cases

2. **Use Explicit Request**:
   - Ask OpenCode directly: "Use [skill-name] for this task"
   - Or: "Load the [skill-name] skill"

3. **Review Keywords**:
   - Skills with clear keywords in description trigger more reliably
   - Check that description includes relevant action words

### Performance Issues

**Problem**: OpenCode slow with many skills installed

**Solutions**:

1. **Install Only Needed Skills**:
   ```bash
   # Install specific skills instead of all
   ./scripts/install_opencode_skills.sh --global skill-name
   ```

2. **Use Project-Local for Active Projects**:
   ```bash
   # Install only project-relevant skills
   ./scripts/install_opencode_skills.sh --project skill-name
   ```

3. **Remove Unused Skills**:
   ```bash
   # Remove from global install
   rm -rf ~/.config/opencode/skill/unused-skill
   ```

### Getting More Help

If issues persist:
1. Check [GitHub Issues](https://github.com/sst/opencode/issues)
2. Review [OpenCode Documentation](https://opencode.ai/docs/skills/)
3. Open a new issue with:
   - OpenCode version: `opencode --version`
   - Skill name and version (if applicable)
   - Error message or screenshot
   - Steps to reproduce

For more information, see [OpenCode Skills Documentation](https://opencode.ai/docs/skills/).
