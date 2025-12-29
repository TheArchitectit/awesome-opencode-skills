# Testing Procedure for OpenCode Skills Migration

This document outlines the testing steps for verifying the migrated OpenCode skills work correctly.

## Prerequisites

1. OpenCode v1.0.207+ installed ✅
2. No existing OpenCode skills installed ✅

## Test Plan

### Phase 1: Install Skills

**Test 1.1: Global Installation**
```bash
# Install all skills to global config
./scripts/install_opencode_skills.sh --global
```

**Expected Result:**
- Directory created: `~/.config/opencode/skill/`
- All 24+ skills copied successfully
- Success message shown

**Verify:**
```bash
ls ~/.config/opencode/skill/ | wc -l
# Should show 24+ entries
```

### Phase 2: Start OpenCode and Verify Discovery

**Test 2.1: Start OpenCode**
```bash
opencode
```

**Expected Result:**
- OpenCode TUI starts successfully
- No errors or warnings during startup

**Test 2.2: Check Skill Discovery**
In OpenCode, use `/skills` command or check available skills

**Expected Result:**
- All 24+ skills appear in skill list
- Skills have correct names and descriptions
- No duplicate skills

**Verify:**
- Skill count matches expected
- Skill names are correct (no "Claude" references)
- Descriptions are accurate

### Phase 3: Load and Test Individual Skills

**Test 3.1: Load skill-creator**
- Request: "I want to create a new skill"
- Expected: skill-creator loads automatically
- Verify: Instructions appear, no errors

**Test 3.2: Load brand-guidelines**
- Request: "Apply OpenCode branding to this presentation"
- Expected: brand-guidelines loads
- Verify: Colors and typography guidelines appear

**Test 3.3: Load a document skill**
- Request: "Help me work with this PDF file"
- Expected: document-skills/pdf loads
- Verify: PDF workflow instructions appear

### Phase 4: Test Installation Script

**Test 4.1: Project-local installation**
```bash
cd /tmp/test-project
./path/to/awesome-opencode-skills/scripts/install_opencode_skills.sh --project webapp-testing
```

**Expected Result:**
- `.opencode/skill/webapp-testing/` directory created
- Skill copied successfully

**Test 4.2: Individual skill installation**
```bash
./path/to/awesome-opencode-skills/scripts/install_opencode_skills.sh --global brand-guidelines
```

**Expected Result:**
- Only brand-guidelines skill installed globally
- Success message confirms installation

### Phase 5: Verify No Claude References

**Test 5.1: Check skill descriptions**
- Load 5 random skills
- Verify: No "Claude", "Claude.ai", or "Anthropic" in descriptions

**Test 5.2: Check README**
- Read README.md
- Verify: No Claude/Anthropic/Composio branding

**Test 5.3: Check CONTRIBUTING.md**
- Read CONTRIBUTING.md
- Verify: References OpenCode community

### Phase 6: Validate Skill Format

**Test 6.1: Run validation on all skills**
```bash
for dir in */SKILL.md document-skills/*/SKILL.md; do
  python3 skill-creator/scripts/quick_validate.py "$(dirname $dir)"
done
```

**Expected Result:**
- All skills show "✅ Skill is valid!"
- No validation errors

## Success Criteria

Migration is successful when:

1. ✅ All 24+ skills install to global directory
2. ✅ OpenCode discovers all installed skills
3. ✅ No Claude/Anthropic branding visible in OpenCode
4. ✅ Skills load without errors
5. ✅ Skill descriptions are accurate
6. ✅ Installation scripts work correctly

## Issues Found

Document any issues discovered during testing:

| Skill | Issue | Severity | Status |
|--------|-------|----------|--------|
|        |       |          |        |

## Test Results

Complete after testing session:

- **Date**: [YYYY-MM-DD]
- **OpenCode Version**: [vX.X.X]
- **Skills Tested**: [X of 24]
- **Passed**: [X]
- **Failed**: [X]
- **Overall**: [PASS/FAIL]

## Notes

[Additional notes or observations during testing]
