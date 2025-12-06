---
type: command
name: code-review
description: Execute code review with priority-based feedback
usage:
  - /code-review path/to/file.ts
  - /code-review src/features/
  - /code-review feature/branch-name
  - /code-review
---
# Code Review Command

Execute code review and provide priority-based feedback.

## Usage

```bash
/code-review path/to/file.ts       # Specific file
/code-review src/features/         # Directory
/code-review feature/branch-name   # Diff between specific branch and main/master
/code-review                       # No argument (see below)
```

No argument behavior:
- Not on main/master → Diff between current branch and main/master
- On main/master → Staged and unstaged changes

## Prerequisites

Verify the following before execution. Abort and report reason if not met:

1. Target files exist
2. `.ai/context.md` is readable
3. `.ai/references/checklists/code-review.md` exists

## Execution Steps

### 1. Identify Target and Assess Scale
- Argument is file/directory → Use that path
- Argument is branch name → Get diff from main/master
- No argument → Determine current branch and follow above rules
- **Scale assessment**:
  - Check number of changed files and total changed lines
  - For large changes (50+ files or 1000+ lines):
    - Notify user, propose Critical/High only first
    - If accepted: Critical/High → Report → Medium/Low separately
    - If declined: Review all at once (warn about time required)

### 2. Collect Domain Knowledge
- Check context.md constraints and critical areas
- Collect domain knowledge from docs/ (if exists)
- Identify critical domains (payment, auth, etc.)

### 3. Run Automated Checks
- Run tests, lint, build
- **On failure, prompt fixes and abort review**
- Start review after passing

### 4. Execute Review
- Load `.ai/references/checklists/code-review.md`
- Load all files linked via "→ Definition:" in checklist
- Check in order: Critical → High → Medium → Low
- Leverage MR description context (research, execution plans) to evaluate design decisions
- For deviations from common patterns, present alternatives (include rejection as an option even when recommending the current approach)
- Apply strict checks on critical domains (see below)

### 5. Self-Reflection

Before outputting results, re-verify each issue against these criteria.
Remove inaccurate ones and adjust scores:

1. **Location verification**: Does the specified `file:line` contain the cited code?
   - Not found → Remove (confidence 0)

2. **Syntax verification**: Would applying the fix cause syntax errors?
   - Would cause error → Fix the suggestion or remove

3. **Context consistency**: Does the fix conflict with surrounding code/existing implementation?
   - Conflicts → Lower confidence (-2 to 3)

4. **Deduplication**: Are there multiple issues pointing to the same problem?
   - Duplicates found → Merge into most appropriate one

5. **Over-reporting filter**: Remove issues matching:
   - Auto-fixable by lint/formatter
   - Merely pushing style preferences
   - Asserting "should do X" without clear rationale

### 6. Output Results
- Report following the output format below

## Output Format

```markdown
# Code Review Results: [target]

## Critical
### 1. `file.ts:42` - [Brief problem description] (Confidence: 9/10)

**Problem**: [Specific issue]
**Rationale**: [Why this is problematic - cite specific code]

**Fix Options**:
| Option | Overview | Reason |
|--------|----------|--------|
| A (recommended) | [Fix A] | [Why this is most recommended] |
| B | [Fix B] | [Pros and cons] |

## High / Medium / Low
(Same format)

## Summary
Issues: Critical X, High X, Medium X, Low X
Next Actions: [Recommendations]

## Referenced Documents
- `.ai/references/checklists/code-review.md`
- `.ai/references/glossaries/xxx.md`
- (List all loaded documents)
```

### Required Fields

Each issue must include:

| Field | Description |
|-------|-------------|
| File:line | Accurate location (verified to exist) |
| Problem | What's wrong (1-2 sentences) |
| Confidence | Score 1-10 |
| Rationale | Why it's problematic (must cite code) |
| Fix options table | Options, overview, reason (mark recommended) |

### Confidence Criteria

| Score | Meaning | Examples |
|-------|---------|----------|
| 9-10 | Clear problem | Bug, security vulnerability, data loss risk |
| 7-8 | High confidence problem | N+1 query, unhandled exception, missed edge case |
| 5-6 | Improvement recommended | Poor readability, mixed responsibilities, insufficient tests |
| 3-4 | Suggestion level | Naming improvements, refactoring candidates |
| 1-2 | For reference | Alternative approaches, future considerations |

**Note**: Confidence 5 or below means "debatable." Can be rejected if reviewee's intentional choice.

## Success Criteria

This command execution is considered successful when:

1. Issues organized by priority (Critical/High/Medium/Low)
2. Each issue includes confidence score, rationale, and specific fix options
3. Automated checks (tests, lint, build) passed
4. Self-reflection performed and inaccurate issues removed

## Critical Domain Rules

Apply strict checks for code under critical domains defined in context.md or docs/:

- **Idempotency**: Safe to send same request twice
- **Transaction management**: Multi-updates are atomic
- **High test coverage**: Critical logic covers all patterns
- **Error handling**: Explicit handling of timeout, network errors, etc.

## Completion Checklist

Verify all items before reporting. Fix incomplete items before reporting:

- [ ] All prerequisites met
- [ ] Ran automated checks (tests, lint, build)
- [ ] Verified all checklist items
- [ ] Loaded all "→ Definition:" linked files in checklist
- [ ] Line numbers are accurate (cited code exists)
- [ ] Each issue has confidence score and rationale
- [ ] Self-reflection removed duplicates/over-reported issues
- [ ] Proposed staged review for large changes
- [ ] Priority levels (Critical/High/Medium/Low) appropriate
- [ ] Followed output format
- [ ] Listed all referenced documents

## Principles

- Clear priorities, present specific fixes with rationale
- Avoid vague feedback, subjective preferences, lint-automatable issues

## Related

- `/review-update` - Reflect review learnings to checklist/command
