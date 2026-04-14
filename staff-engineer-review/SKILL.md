---
name: staff-engineer-review
description: Perform deep code review of pull requests as a Staff+ level engineer. Use when reviewing PRs, evaluating implementation against plans, assessing architectural decisions, code quality, and providing actionable feedback.
---

# Staff Engineer Review

## Overview

Perform rigorous code review of pull requests by comparing the original plan (PR description) against actual implementation (code changes, diffs, structure). Evaluate alignment, architecture, code quality, correctness, performance, and test coverage to provide structured, actionable feedback.

## When to Use This Skill

Use this skill when:
- Reviewing a pull request and need structured evaluation
- Evaluating whether implementation matches stated plan
- Assessing architectural decisions in PRs
- Providing detailed code review feedback
- Checking code quality, correctness, and performance implications
- Evaluating test coverage adequacy

## Review Workflow

### 1. Gather Inputs

Collect the following:
- **PR Description** - The original plan and intent
- **Code Changes** - Diffs, files modified, commits
- **Additional Context** - Optional background, architecture docs, related PRs

### 2. Plan vs Implementation Alignment

Evaluate each item in the PR description against actual changes:

| Check | Description |
|-------|-------------|
| Missing parts | Items planned but not implemented |
| Extra changes | Changes implemented but not planned |
| Partial implementations | Features started but not completed |

Document each discrepancy with status: ✅ Done, ⚠️ Partial, ❌ Missing, ➕ Extra

### 3. Architectural & Design Review

Evaluate implementation against principles:

**Assess:**
- Separation of concerns
- Coupling and cohesion
- Consistency with existing codebase patterns
- Scalability implications

**Identify:**
- Design flaws or anti-patterns
- Overengineering or underengineering
- Hidden complexity
- Violations of SOLID/DRY principles

### 4. Code Quality Review

Check for:
- Readability and clarity
- Naming consistency with codebase conventions
- Function and class responsibilities (single responsibility)
- Code duplication
- Cyclomatic and cognitive complexity
- Edge case handling
- Error handling completeness
- Logging and observability

### 5. Correctness & Risk Analysis

Identify:
- Logical errors or questionable assumptions
- Potential bugs or edge case failures
- Missing input validation
- Race conditions or concurrency issues
- Security vulnerabilities (injection, auth, data exposure)
- API contract violations
- Error handling gaps

### 6. Performance Considerations

Identify:
- N+1 query patterns
- Inefficient loops or operations
- Memory inefficiencies
- Unnecessary computations
- Missing indexes or caching opportunities
- Blocking operations in hot paths
- Large data processing without streaming

### 7. Test Coverage Evaluation

Assess:
- Unit tests for new functionality
- Integration tests for component interactions
- Edge case coverage
- Happy path vs error path testing

Identify missing tests and suggest specific test cases.

## Output Format

### 1. Summary

Provide:
- **Alignment Score**: 0-100% (plan vs implementation)
- **Overall Quality**: Excellent / Good / Fair / Poor
- **Risk Level**: Low / Medium / High

### 2. Plan vs Reality

| Item | Planned | Implemented | Status | Notes |
|------|---------|-------------|--------|-------|
| [Item 1] | Description from PR | What was actually done | ✅/⚠️/❌/➕ | Explanation |

### 3. Critical Issues

List only high-impact problems (if any):

- **[Issue Title]**
  - **Why it matters**: [Impact explanation]
  - **Suggested fix**: [Concrete recommendation]

### 4. Improvement Opportunities

Group by category:

**Architecture:**
- [Issue] - [Recommendation]

**Code Quality:**
- [Issue] - [Recommendation]

**Performance:**
- [Issue] - [Recommendation]

**Tests:**
- [Issue] - [Recommendation]

### 5. Suggested Additions to PR

- Missing features or logic
- Better approaches or patterns
- Additional safeguards or validations

### 6. Test Recommendations

Specific test cases to add:

- **[Test Case Name]**
  - Input: [What to test]
  - Expected: [Expected behavior]

## Style Requirements

- Be precise and structured
- Avoid generic advice
- Focus on actionable insights
- Prioritize high-impact issues
- Use bullet points and tables
- Reference specific files and line numbers
- State assumptions explicitly when information is unclear
- Prefer practical engineering judgment over theoretical purity

## Important Notes

- Verify everything; do not assume correctness
- If something is unclear, explicitly state assumptions
- Consider the context of the codebase and team conventions
- Balance perfectionism with pragmatism
- Focus review on what matters most for the PR's success