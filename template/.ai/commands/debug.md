---
type: command
name: debug
description: Support bug investigation and identify root causes with fix proposals
usage:
  - /debug TypeError: Cannot read property 'x' of undefined
  - /debug Session expires after login
  - /debug logs/error.log
---
# Debug Command

Support bug investigation and identify root causes with fix proposals.

## Usage

```bash
/debug TypeError: Cannot read property 'x' of undefined
/debug Session expires after login
/debug logs/error.log
```

## Prerequisites

Verify the following before execution. Abort and report reason if not met:

1. Error message, symptom, or log file is provided
2. Related source code is accessible

## Execution Steps

### 1. Understand Situation
- Analyze error message/stack trace
- Confirm reproduction steps, frequency, impact scope
- Insert `[NEEDS CLARIFICATION: question]` for unclear points (max 3)

### 2. Identify Cause
- Investigate error location and related code
- Form hypothesis (direct cause → root cause)
- Verify with logs/debugger

### 3. Determine Response

| Type | Response |
|------|----------|
| Simple bug (typo, null check missing, etc.) | Fix immediately + add tests |
| Technical debt (design flaw) | Patch + record in docs/ |

### 4. Output Results
- Report following the output format below

## Output Format

```markdown
# Debug Report

## Problem: [Symptom]
## Cause: Direct=[X], Root=[Y]
## Classification: [Simple bug/Technical debt]

## Fix Proposal
[Specific fix content]

## Tests to Add
[Test cases to add]

## Next Actions
1. [Step]
```

## Success Criteria

This command execution is considered successful when:

1. Direct cause and root cause clearly distinguished and identified
2. Fix proposal is specific (includes file name, line number, code example)
3. Test addition proposal for preventing recurrence is provided

## Common Patterns

| Error | Cause | Check |
|-------|-------|-------|
| null/undefined | Missing initialization, async | Data flow |
| Type error | Type conversion, API response | Input/output types |
| N+1 | Missing eager loading | Query log |

## Completion Checklist

Verify all items before reporting. Fix incomplete items before reporting:

- [ ] All prerequisites met
- [ ] Direct cause and root cause clearly distinguished
- [ ] Fix proposal is specific (file name, line number, code example)
- [ ] Test addition proposal included
- [ ] Followed output format
- [ ] Asked user for clarification if `[NEEDS CLARIFICATION]` remains

## Principles

5 Whys, hypothesis-driven, minimal reproduction
