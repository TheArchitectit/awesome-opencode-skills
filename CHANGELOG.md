# Changelog

All notable changes to the Awesome OpenCode Skills collection are documented here.

## [1.3.0] - 2026-08-04

### ✨ New Skills (14 vendored, >500★, free, permissive license)

Vendored from popular standalone repos referenced by the `awesome-claude-skills` upstream, each carrying its own LICENSE for attribution (see `CREDITS.md`):

- **Playwright Browser Automation** (`playwright-skill`) — 2,972★, MIT · Complete browser automation with Playwright
- **Skill Seekers** (`skill-seekers`) — 14,687★, MIT · Auto-build skills from docs, repos, PDFs, videos
- **lean-ctx** (`lean-ctx`) — 3,484★, Apache-2.0 · Context engineering / MCP context runtime
- **iOS Simulator** (`ios-simulator-skill`) — 1,198★, MIT · 29 scripts for iOS app testing via simulator
- **Superpowers** (obra/superpowers, MIT, 265,830★): `finishing-a-development-branch`, `using-git-worktrees`, `test-driven-development`, `brainstorming`
- **Tapestry** (michalparkola/tapestry-skills-for-claude-code, MIT, 511★): `article-extractor`, `youtube-transcript`, `ship-learn-next`
- **Claude Skills Marketplace** (mhattingpete/claude-skills-marketplace, Apache-2.0, 656★): `git-pushing`, `review-implementing`, `test-fixing`

### 🔧 Improvements

- **License/credit enforcement**: Added `scripts/check_skills.sh` — a pre-commit gate that verifies every skill has a LICENSE, valid SKILL.md frontmatter, no stale branding (allowlist-aware, `--strict` to gate), and that `skills.json` matches disk. Installed as a `pre-commit` git hook. Added `scripts/branding-allowlist.txt` for legitimate functional refs (Anthropic SDK imports, `author="Claude"` defaults, `--agent claude` CLI flag).
- **Attribution manifest**: Added `CREDITS.md` documenting source repo + license + stars for every vendored skill.
- **Skills registry**: Expanded `.opencode/skills.json` from 31 → 45 registered skills (version 1.2.0 → 1.3.0).
- **Playwright rebrand**: Fixed supporting files (`API_REFERENCE.md`, `package.json`, `run.js`) missed in initial batch.
- **Document skills**: Preserved original Anthropic proprietary LICENSE headers (not swapped to Apache).

## [1.2.0] - 2026-08-04

### ✨ New Skills

Ported from the `awesome-claude-skills` upstream (ComposioHQ) during a skills audit; rebranded Claude/Anthropic references to OpenCode.

- **LangSmith Fetch** — Debugs LangChain and LangGraph agents by fetching and analyzing execution traces from LangSmith Studio. Investigates errors, tool calls, memory operations, and performance. 📖 Comprehensive → Development & Code Tools
- **Twitter Algorithm Optimizer** — Analyzes and optimizes tweets for maximum reach and engagement using Twitter's open-source algorithm insights (Real-graph, SimClusters, TwHIN, Tweepcred). 📖 Comprehensive → Communication & Writing
- **Tailored Resume Generator** — Analyzes job descriptions and generates tailored resumes highlighting relevant experience, skills, and achievements to maximize interview chances, with ATS optimization. 📖 Comprehensive → Productivity & Organization

### 🔧 Improvements

- **Skills registry**: Expanded `.opencode/skills.json` from 28 → 31 registered skills
- **README completeness**: Added the 3 new skills to their category listings (Development, Communication & Writing, Productivity & Organization)
- **Upstream audit**: Compared against `ComposioHQ/awesome-claude-skills` upstream; all 23 shared skills confirmed in sync (upstream unchanged since 2025-11-19). The remaining in-repo gaps (`connect`, `connect-apps`, `connect-apps-plugin`) are Composio-product-dependent and intentionally excluded.

## [1.1.0] - 2026-06-02

### ✨ New Skills

- **Staff Engineer Review** — Deep code review of pull requests as a Staff+ engineer, evaluating alignment, architecture, code quality, correctness, performance, and test coverage
- **Code Security Auditor** — Pre-execution security audits of untrusted codebases through static analysis to identify supply chain risks and security vulnerabilities

### 🐛 Bug Fixes

- **Branding cleanup**: Replaced all remaining Claude/Anthropic references across skill content with OpenCode equivalents
  - `artifacts-builder` — replaced "claude.ai HTML artifacts" with "OpenCode HTML artifacts"
  - `developer-growth-analysis` — replaced `~/.claude/history.jsonl` with `~/.config/opencode/history.jsonl`
  - `document-skills/docx/ooxml.md` — replaced `w:author="Claude"` with `w:author="OpenCode"` in tracked change examples
  - `mcp-builder/reference/evaluation.md` — replaced `pip install anthropic`, `ANTHROPIC_API_KEY`, and Claude model references
  - `mcp-builder/reference/mcp_best_practices.md` — replaced "Claude Desktop" with "OpenCode Desktop"
  - `skill-creator` — replaced "AI capabilities" with "OpenCode capabilities"

- **Description format fixes**: Cleaned up YAML frontmatter across document skills
  - Removed unnecessary quotes around description values in docx, pptx, xlsx
  - Rewrote internal-comms description from first-person ("help me write") to third-person ("help users write")

### 🔧 Improvements

- **Skills registry**: Expanded `.opencode/skills.json` from 9 → 30 registered skills, adding all missing entries across every category
- **README completeness**: Added missing skills to category listings
  - `developer-growth-analysis` → Data & Analysis
  - `skill-share` → Collaboration & Project Management
- **Path convention documentation**: Updated README, OPENCODE_SKILLS.md, and MIGRATION.md to document both official paths
  - `.opencode/skills/` (official, recommended) and `.opencode/skill/` (also supported)
  - `~/.config/opencode/skills/` (global, recommended) and `~/.config/opencode/skill/` (global, also supported)
  - Backward compatible: `.claude/skills/` for migration
- **MCP server**: Windows compatibility fixes, FastMCP entrypoint/runtime fixes
- **Referral links**: Added support referral links with proper formatting

## [1.0.0] - 2025-01-20

### ✨ Initial Release

- Migrated from awesome-claude-skills to OpenCode branding
- 28 skills across 9 categories:
  - **Document Processing**: docx, pdf, pptx, xlsx
  - **Development & Code Tools**: artifacts-builder, changelog-generator, mcp-builder, skill-creator, webapp-testing
  - **Business & Marketing**: brand-guidelines, competitive-ads-extractor, domain-name-brainstormer, internal-comms, lead-research-assistant
  - **Communication & Writing**: content-research-writer, meeting-insights-analyzer
  - **Creative & Media**: canvas-design, image-enhancer, slack-gif-creator, theme-factory, video-downloader
  - **Productivity & Organization**: file-organizer, invoice-organizer, raffle-winner-picker
  - **Security & Systems**: (coming soon)
- MCP skill management server (TypeScript and Python)
- Installation helper script
- Skills metadata and index documentation
