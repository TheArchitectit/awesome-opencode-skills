---
name: code-security-auditor
description: Perform pre-execution security audits of untrusted codebases through static analysis. Use when analyzing a codebase for potential malicious behavior, supply chain risks, or security vulnerabilities before local execution. Triggered by requests like "analyze this project for security risks", "audit this code before running", "check if this codebase is safe", or similar security review requests.
---

# Code Security Auditor

## Overview

This skill enables OpenCode to perform a comprehensive pre-execution security audit of a given codebase and produce a structured, high-signal risk report. It analyzes the entire project including source code, dependency manifests, build scripts, and configuration files from a security-first perspective.

## When to Use This Skill

Use this skill when:
- User requests security analysis of a codebase
- User asks to "audit", "scan", or "check" code for safety before running
- User wants to know if code is safe to execute locally
- Analyzing untrusted or third-party code
- Performing due diligence on new dependencies or projects

## Analysis Workflow

### Step 1: Understand the Project Scope

1. Identify the primary language and ecosystem (JavaScript/Node, Python, Go, Ruby, etc.)
2. Locate all dependency manifests:
   - `package.json`, `package-lock.json` (Node.js)
   - `requirements.txt`, `Pipfile`, `pyproject.toml` (Python)
   - `Gemfile`, `Gemfile.lock` (Ruby)
   - `go.mod`, `go.sum` (Go)
   - `Cargo.toml` (Rust)
   - `pom.xml`, `build.gradle`, `build.gradle.kts` (Java/Kotlin)
3. Identify entry points: main scripts, entry files, startup commands

### Step 2: Perform Static Analysis

#### 1. Dependencies Audit

Scan dependency manifests for:
- Known malicious or compromised packages (check known malware databases)
- Unmaintained packages (no recent updates, abandoned repos)
- Newly published packages (< 30 days) with high download counts
- Typosquatting risks (packages with similar names to popular libraries)
- Packages with install-time scripts (`preinstall`, `postinstall`, `prepare`, `prepublish`)

Reference: Use `references/package_checks.md` for known suspicious packages and patterns.

#### 2. Script Inspection

Examine all scripts for:
- Lifecycle hooks in manifest files (`postinstall`, `preinstall`, `prepare`, `prepublish`)
- Shell execution patterns: `exec`, `spawn`, backticks, `system()`, `os.system()`, `subprocess` calls
- Dynamic code execution: `eval()`, `Function()`, `setTimeout()` with strings, `pickle.loads()`, `unserialize()`
- Encoded payloads: base64, hex, obfuscated strings, string concatenation
- Download and execute patterns: curl/wget piping to shell

#### 3. File System Behavior

Detect operations that:
- Write outside the project directory
- Access sensitive paths: `~/.ssh`, `~/.aws`, `/etc`, `/var`, `/proc`, `/sys`
- Create hidden files: dotfiles in home directory, startup scripts
- Modify system configuration: cron, systemd services, launch agents

#### 4. Network Activity

Identify:
- Hardcoded IP addresses (especially external)
- Hardcoded domains and endpoints
- Suspicious URL patterns: data exfiltration endpoints, command-and-control
- Unexpected ports or protocols
- DNS lookups or reverse IP queries

#### 5. Obfuscation and Evasion

Flag:
- Minified or obfuscated code (especially in dependencies)
- Anti-debugging techniques: debugger detection, stack trace manipulation
- Dynamic imports: `import()`, `require()` with variable paths
- Runtime code generation: `eval()`, `new Function()`, `createElement` with strings

### Step 3: Risk Assessment

For each finding, assess:
- **Impact**: What can happen if this code runs locally?
- **Likelihood**: How likely is this to be malicious vs. legitimate?
- **Evidence**: Specific file, line number, and code snippet

#### Potential Impact Categories

- **File system compromise**: Code that writes to arbitrary locations
- **Credential theft**: Access to SSH keys, environment variables, tokens, passwords
- **Remote command execution**: Network-enabled code execution capabilities
- **Persistence**: Cron jobs, startup scripts, systemd services, launch agents
- **Privilege escalation**: Code that requests or attempts to gain elevated privileges
- **Data exfiltration**: Network transmission of sensitive data

### Step 4: Generate Structured Report

Produce output following the strict format in Output Format section.

## Output Format

### 🔴 Critical Risks

Provide each critical risk with:
- **Risk title**: Brief descriptive title
- **Evidence**: File path, line number, specific code snippet
- **Why it is dangerous**: Technical explanation of the risk
- **What to verify manually**: Steps to confirm the finding

### 🟠 Suspicious Findings

Same structure as critical risks but lower severity.

### 🟡 Low Risk / Observations

Interesting findings that don't pose immediate danger but worth noting.

### 🔍 Manual Review Checklist

Provide actionable checklist items:
- [ ] Verify specific package legitimacy
- [ ] Check maintainer reputation
- [ ] Review network connections
- [ ] Audit file system operations
- etc.

### 🚨 Indicators of Malicious Intent

List specific patterns that strongly indicate malicious code:
- Obfuscated code executing commands
- Suspicious network exfiltration
- Persistence mechanism installation
- Credential harvesting patterns

### 🧾 Final Verdict

Choose ONE and provide justification:
- **SAFE TO RUN**: No significant risks identified
- **SAFE WITH SANDBOX ONLY**: Risks exist but contained by sandbox
- **HIGH RISK — DO NOT RUN**: Significant malicious indicators found

## Constraints

- DO NOT assume code is safe
- DO NOT execute any code
- DO NOT skip files
- Prefer false positives over false negatives
- Document all findings, even minor ones

## Resources

### scripts/

This skill does not require executable scripts.

### references/

- `package_checks.md`: Reference for known suspicious packages, malware patterns, and risky dependency indicators

### assets/

This skill does not require assets.
