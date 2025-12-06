---
type: command
name: review-update
description: Reflect code review learnings to checklist and command
usage:
  - /review-update
---

# Review Update Command

Reflect on code review session and improve checklist and command.

## Target Files

- `.ai/references/checklists/code-review.md` - Check items
- `.ai/commands/code-review.md` - Review flow

## Prerequisites

Verify the following before execution. Abort and report reason if not met:

1. Code review session was just conducted
2. `.ai/references/checklists/code-review.md` exists
3. Session contains learnings worth saving

## Execution Steps

### 1. Extract
Identify content to save from session:
- New review perspectives (security, performance, etc.)
- Effective patterns and anti-patterns with examples
- Repeatedly raised problems
- Review flow improvements

### 2. Consistency Check
- Verify no contradictions/duplicates with existing items
- Verify priority (Critical/High/Medium/Low) appropriateness

### 3. Size Check
```bash
python3 .ai/scripts/measure-context.py --references
```
Compress before adding if threshold exceeded.

### 4. Determine Save Location

| Type | Location |
|------|----------|
| Check items, pattern examples | .ai/references/checklists/code-review.md |
| Review flow, output format | .ai/commands/code-review.md |

### 5. Sync
```bash
python3 .ai/scripts/sync-context.py
```

## Compression Strategy
1. Merge duplicates (combine similar check items)
2. Simplify expressions
3. Raise priority for frequently occurring items
4. Remove ineffective pattern examples

## Output Format
```
### Change Summary
- Checklist: Added X, Modified X, Deleted X
- Command: Added/Modified/No change
- Compression: Done/Not needed

### Updates
[Diff or added items]
```

## Success Criteria

This command execution is considered successful when:

1. Review learnings saved in form usable for future reviews
2. Added items are specific and verifiable (include Good/Bad examples)
3. Checklist remains within threshold

## Completion Checklist

Verify all items before reporting. Fix incomplete items before reporting:

- [ ] All prerequisites met
- [ ] Added items are specific and verifiable
- [ ] No contradictions/duplicates with existing items
- [ ] Priority properly assigned
- [ ] Ran size check, within threshold
- [ ] Followed output format

## Principles

- Prioritize concrete fix examples (Good/Bad)
- Only practical knowledge needed (no historical context or opposing concepts for comparison)
- Project-specific items go to context.md
- Generic best practices go to checklist

## Related

- `/code-review` - Execute code review
