# Package Security Reference

## Known Malicious Packages

### npm / JavaScript

| Package | Indicator | Notes |
|---------|-----------|-------|
| `pluggable-json` | Typosquat of `printable-json` | Data exfiltration |
| `babel-node` (unofficial) | Typosquat | Malware distribution |
| `eslint-scope` (compromised) | Historical supply chain attack | Credential theft |
| `event-stream` (compromised) | Famous attack | Bitcoin stealing |
| `flatmap-stream` | Embedded in event-stream attack | Cryptocurrency theft |
| `crossenv` | Typosquat of `cross-env` | Malware distribution |
| `hueter-json` | Typosquat | Suspicious behavior |

### PyPI / Python

| Package | Indicator | Notes |
|---------|-----------|-------|
| `reqs` | Typosquat of `reqwest` | Malware |
| `pyyaml` (unofficial) | Typosquat | Backdoor |
| `requests` (typo variants) | Typosquat | Various attacks |

## Suspicious Patterns

### Install-Time Scripts

Red flags in package.json:
- `postinstall`: Code runs after `npm install`
- `preinstall`: Pre-installation hooks
- `prepare`: Development dependency hook
- `prepublish`: Publishing hook

### Network Indicators

Suspicious patterns:
- Hardcoded IP addresses (especially non-local)
- Base64-encoded domains
- DNS lookups for reconnaissance
- Data发送到 external servers
- Command and control patterns

### File System Red Flags

Dangerous operations:
- Writing to `~/.npmrc`, `~/.ssh/`, `~/.aws/`
- Modifying `/etc/hosts`
- Creating cron jobs
- Writing to `~/Library/LaunchAgents/`
- Modifying systemd services

## Quick Checks

1. **Age**: Package published < 30 days with high download count = suspicious
2. **Maintainer**: Single maintainer with no history = suspicious
3. **Dependencies**: Heavy dependency tree = attack surface
4. **Repository**: No GitHub link or dead link = suspicious
5. **License**: No license or proprietary = investigate further
