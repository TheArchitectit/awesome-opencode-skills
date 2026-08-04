# OpenCode Handoff (P2P)

This is a snapshot of the [opencode-handoff-p2p](https://github.com/Eldorado-ling/opencode-handoff-p2p) skill, which lets you transfer OpenCode session share URLs between machines or collaborators peer-to-peer via personal GitHub private inbox repositories.

## Quick install

```bash
git clone https://github.com/Eldorado-ling/opencode-handoff-p2p \
          ~/.config/opencode/skills/opencode-handoff-p2p
```

Then follow the full deployment guide in the main repo:
- **[README](https://github.com/Eldorado-ling/opencode-handoff-p2p#readme)** — overview, architecture, security model
- **[INSTALL](https://github.com/Eldorado-ling/opencode-handoff-p2p/blob/main/INSTALL.md)** — step-by-step deployment (minimal + hardened paths)
- **[USAGE](https://github.com/Eldorado-ling/opencode-handoff-p2p/blob/main/USAGE.md)** — daily workflow + troubleshooting

## What's in this folder

- `SKILL.md` — the protocol the agent reads
- `verify_inbox.py` — reference verification script (Python)
- `README.md` — this file

The full project also includes `INSTALL.md`, `USAGE.md`, `trust.json.example`, `config.json.example`, `LICENSE`, `CHANGELOG.md` — see the main repo.

## License

MIT (see [LICENSE](https://github.com/Eldorado-ling/opencode-handoff-p2p/blob/main/LICENSE) in main repo).
