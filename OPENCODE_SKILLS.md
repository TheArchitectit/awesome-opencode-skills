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

For more information, see [OpenCode Skills Documentation](https://opencode.ai/docs/skills/).
