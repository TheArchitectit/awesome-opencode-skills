# Skill Credits & Licenses

This manifest records the origin and license of every skill in this repository,
so credit is preserved for all migrated content. The `scripts/check_skills.sh`
pre-commit hook verifies that each skill directory carries a LICENSE and that
this manifest is kept in sync.

## Naming convention

- **In-repo (upstream shared repo):** skills inherited from the
  `ComposioHQ/awesome-claude-skills` upstream. The whole upstream repo is
  Apache-2.0; in-repo skills carry the Apache-2.0 `LICENSE.txt` and derive from
  the same codebase.
- **Vendored (standalone repo):** skills copied from an external GitHub repo.
  Each carries that repo's own LICENSE (MIT / Apache-2.0) for attribution.

## Standalone-repo credits (>500★, free, permissive license)

| Skill dir | Source repo | License | ★ |
| ----------- | ------------- | --------- | --: |
| `playwright-skill` | lackeyjb/playwright-skill | MIT | 2,972 |
| `ios-simulator-skill` | conorluddy/ios-simulator-skill | MIT | 1,198 |
| `skill-seekers` | yusufkaraaslan/Skill_Seekers | MIT | 14,687 |
| `lean-ctx` | yvgude/lean-ctx | Apache-2.0 | 3,484 |
| `article-extractor` | michalparkola/tapestry-skills-for-claude-code | MIT | 511 |
| `youtube-transcript` | michalparkola/tapestry-skills-for-claude-code | MIT | 511 |
| `ship-learn-next` | michalparkola/tapestry-skills-for-claude-code | MIT | 511 |
| `finishing-a-development-branch` | obra/superpowers | MIT | 265,830 |
| `using-git-worktrees` | obra/superpowers | MIT | 265,830 |
| `test-driven-development` | obra/superpowers | MIT | 265,830 |
| `brainstorming` | obra/superpowers | MIT | 265,830 |
| `git-pushing` | mhattingpete/claude-skills-marketplace | Apache-2.0 | 656 |
| `review-implementing` | mhattingpete/claude-skills-marketplace | Apache-2.0 | 656 |
| `test-fixing` | mhattingpete/claude-skills-marketplace | Apache-2.0 | 656 |

## Upstream-repo credits (in-repo, Apache-2.0)

| Skill dir | Source | License |
|-----------|--------|---------|
| `artifacts-builder`, `brand-guidelines`, `canvas-design`, `changelog-generator`, `competitive-ads-extractor`, `content-research-writer`, `developer-growth-analysis`, `document-skills/*`, `domain-name-brainstormer`, `file-organizer`, `image-enhancer`, `internal-comms`, `invoice-organizer`, `langsmith-fetch`, `lead-research-assistant`, `mcp-builder`, `meeting-insights-analyzer`, `raffle-winner-picker`, `skill-creator`, `skill-share`, `slack-gif-creator`, `tailored-resume-generator`, `theme-factory`, `twitter-algorithm-optimizer`, `video-downloader`, `webapp-testing` | ComposioHQ/awesome-claude-skills | Apache-2.0 |

## Add a new skill

1. Copy the skill source into a top-level `<skill>/` directory.
2. Include the upstream `LICENSE` (or add Apache-2.0 `LICENSE.txt` for in-repo).
3. Add a row to the relevant credits table above.
4. Run `./scripts/check_skills.sh --strict` before committing.
