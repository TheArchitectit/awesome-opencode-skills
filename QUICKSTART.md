# OpenCode Skills Quick Start Guide

This guide helps you get started quickly with common skill combinations and workflows.

## Common Skill Workflows

### 1. Writing & Content Creation

**For Creating Blog Posts or Articles:**

```bash
# Install globally
./scripts/install_opencode_skills.sh --global content-research-writer
```

Then use:
```
Help me write a blog post about [topic] with research and citations
```

**With Artifacts for Visual Content:**

Combine with:
- **content-research-writer** - Research and write content
- **image-enhancer** - Improve screenshots
- **canvas-design** - Create visual art/graphics
- **brand-guidelines** - Apply consistent styling

### 2. Developer Productivity

**For Daily Development Work:**

```bash
# Install globally
./scripts/install_opencode_skills.sh --global skill-creator webapp-testing mcp-builder
```

Use together:
```
Create a new MCP server for [service]
```
→ Tests the server with webapp-testing
→ Creates skill documentation with skill-creator

### 3. Business & Marketing

**For Product Launch or Campaign:**

```bash
# Install globally
./scripts/install_opencode_skills.sh --global \
  domain-name-brainstormer \
  competitive-ads-extractor \
  lead-research-assistant \
  content-research-writer
```

Workflow:
1. **domain-name-brainstormer** - Find domain name
2. **competitive-ads-extractor** - Research competitor ads
3. **lead-research-assistant** - Identify target companies
4. **content-research-writer** - Create marketing content

### 4. Document Processing

**For Professional Document Work:**

```bash
# Install globally
./scripts/install_opencode_skills.sh --global \
  document-skills/docx \
  document-skills/pdf \
  document-skills/pptx \
  brand-guidelines
```

Examples:
```
Edit this Word document with tracked changes
Fill out this PDF form
Apply OpenCode branding to this presentation
```

### 5. Organization & Productivity

**For Cleaning Up Files:**

```bash
# Install globally
./scripts/install_opencode_skills.sh --global \
  file-organizer \
  invoice-organizer
```

Use in sequence:
```
Help me organize my Downloads folder
Organize my invoices for taxes
```

### 6. Testing & Quality Assurance

**For Web Application Development:**

```bash
# Install globally
./scripts/install_opencode_skills.sh --global \
  webapp-testing \
  artifacts-builder \
  changelog-generator
```

Development cycle:
```
Build a React artifact for this feature
Test my webapp with Playwright
Create a changelog from recent commits
```

### 7. Visual & Creative Work

**For Creating Visual Assets:**

```bash
# Install globally
./scripts/install_opencode_skills.sh --global \
  canvas-design \
  slack-gif-creator \
  image-enhancer \
  theme-factory \
  brand-guidelines
```

Creative workflow:
```
Create a poster for [topic]
Make a GIF for Slack from this design
Enhance these screenshots
Apply [theme-name] to the artifact
```

### 8. Meeting & Communication

**For Professional Communication:**

```bash
# Install globally
./scripts/install_opencode_skills.sh --global \
  internal-comms \
  meeting-insights-analyzer \
  content-research-writer
```

Workflow:
```
Write a 3P update for my team
Analyze my meeting transcripts for communication patterns
Help me write an internal announcement
```

### 9. Research & Analysis

**For Research-Heavy Projects:**

```bash
# Install globally
./scripts/install_opencode_skills.sh --global \
  lead-research-assistant \
  competitive-ads-extractor \
  content-research-writer \
  developer-growth-analysis
```

Research workflow:
```
Find leads for my product
Analyze competitor strategies
Write research report with citations
Review my development patterns
```

### 10. Multi-Project Development

**For Managing Multiple Projects:**

```bash
# Install all productivity skills globally
./scripts/install_opencode_skills.sh --global
```

Essential combo:
- **skill-creator** - Create custom skills for your workflows
- **file-organizer** - Keep projects organized
- **changelog-generator** - Document changes
- **webapp-testing** - Test features
- **content-research-writer** - Write documentation

## Skill Categories Quick Reference

| Category | Use Case | Key Skills |
|----------|----------|------------|
| **Writing** | Blog posts, documentation, articles | content-research-writer, internal-comms |
| **Development** | Building tools, MCP servers, testing | skill-creator, mcp-builder, webapp-testing |
| **Business** | Marketing, leads, research | lead-research-assistant, competitive-ads-extractor |
| **Documents** | Office files, PDFs, presentations | docx, pdf, pptx, brand-guidelines |
| **Organization** | File management, invoices, cleanup | file-organizer, invoice-organizer |
| **Visual** | Graphics, GIFs, design | canvas-design, slack-gif-creator, theme-factory |
| **Testing** | Web apps, artifacts, QA | webapp-testing, artifacts-builder |

## Installation Strategies

### Beginner (Quick Start)

Install these 5 essential skills first:
```bash
./scripts/install_opencode_skills.sh --global \
  skill-creator \
  content-research-writer \
  file-organizer \
  document-skills/docx \
  brand-guidelines
```

### Intermediate (Expand Capability)

Add 5-10 more skills based on your needs:
```bash
# For writers & researchers
./scripts/install_opencode_skills.sh --global \
  competitive-ads-extractor \
  lead-research-assistant \
  domain-name-brainstormer

# For developers
./scripts/install_opencode_skills.sh --global \
  mcp-builder \
  webapp-testing \
  changelog-generator \
  artifacts-builder
```

### Advanced (Complete Toolkit)

Install all skills:
```bash
./scripts/install_opencode_skills.sh --global
```

## Getting Help

- **Skill not working?** Check the Troubleshooting section below
- **Need more details?** Read the full SKILL.md file in each skill directory
- **Want to contribute?** See [CONTRIBUTING.md](CONTRIBUTING.md)
- **Have questions?** Open an issue on GitHub

## Next Steps

1. **Start Small** - Try 1-2 skills relevant to your current work
2. **Read Full Docs** - SKILL.md files have detailed instructions
3. **Customize** - Adapt skills to your specific workflows
4. **Combine Skills** - Use multiple skills together for complex tasks
5. **Share Feedback** - Report issues and improvements

## Example: A Complete Workflow

Here's how you might use multiple skills together:

**Scenario:** Launching a new SaaS product

```bash
# Step 1: Find a domain
./scripts/install_opencode_skills.sh --global domain-name-brainstormer

# Step 2: Research competitors
./scripts/install_opencode_skills.sh --global competitive-ads-extractor

# Step 3: Find leads
./scripts/install_opencode_skills.sh --global lead-research-assistant

# Step 4: Create marketing content
./scripts/install_opencode_skills.sh --global content-research-writer

# Step 5: Build landing page artifact
./scripts/install_opencode_skills.sh --global artifacts-builder brand-guidelines

# Step 6: Document changes
./scripts/install_opencode_skills.sh --global changelog-generator
```

Then use OpenCode:
```
Help me brainstorm domain names for [product]
Analyze competitor ads in [industry]
Find 20 qualified leads for this product
Write landing page copy with research citations
Build a branded artifact for the landing page
Create a changelog for our launch
```

**Result:** Comprehensive product launch preparation using 6 specialized skills working together.
