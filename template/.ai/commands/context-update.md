---
type: command
name: context-update
description: Reflect on session and update context files
usage:
  - /context-update
---

# Context Update Command

Reflect on session and update context.

## Premise

- `.ai/context.md` is the single source of truth (SSOT)
- `AGENTS.md`, `CLAUDE.md`, etc. are auto-generated outputs by `sync-context.py`
- Edits must be made to `.ai/context.md`

## Prerequisites

Verify the following before execution. Abort and report reason if not met:

1. `.ai/context.md` exists and is readable
2. Session contains learnings or design decisions worth saving

## Execution Steps

### 1. Extract
Identify content to save:
- New learnings, design decisions and their rationale, pitfalls
- Explanations, feedback, or workflows repeated 3+ times
- Problems repeatedly raised in code reviews

### 2. Consistency Check
- Verify no contradictions, duplicates, or stale information

### 3. Size Check
```bash
python3 .ai/scripts/measure-context.py
```
Compress before adding if threshold exceeded.

### 4. Determine Save Location

| Type | Location |
|------|----------|
| Project-wide rules | .ai/context.md |
| Design decisions (ADR format) | docs/decisions/ |
| Detailed guidelines | docs/guidelines/ |
| New agents/commands | .ai/agents/ or .ai/commands/ |

ADR template: `.ai/references/templates/adr.md`

Agents = dialog/consultation, Commands = action execution. Merge into command if 1:1 correspondence.

### 5. Sync
After updating context.md, sync to tool-specific files:
```bash
python3 .ai/scripts/sync-context.py
```
Sync targets: `AGENTS.md`, `CLAUDE.md`, `.cursor/`, `.github/instructions/`, `.claude/`

## Compression Strategy
1. Merge duplicates  2. Simplify expressions  3. Move details to docs/  4. Remove stale info

## Output Format
```
### Change Summary
- Added/Modified/Deleted: X items, Compression: Done/Not needed

### Updates
[Diff or full content]
```

## Success Criteria

This command execution is considered successful when:

1. Session learnings saved in reusable form
2. context.md within threshold (200 lines or less recommended)
3. No contradictions/duplicates with existing content

## Completion Checklist

Verify all items before reporting. Fix incomplete items before reporting:

- [ ] All prerequisites met
- [ ] Extracted content is specific and reusable
- [ ] No contradictions/duplicates with existing content
- [ ] Ran size check, within threshold
- [ ] Distributed to appropriate save locations
- [ ] Ran `sync-context.py` (or prompted to run)
- [ ] Followed output format

## Principles

- Maximize effect with minimal high-signal information
- Appropriate abstraction level (not too rigid, not too vague)
- Only practical knowledge needed (no historical context or opposing concepts for comparison)
- Add detail links only when separated
- For concepts AI knows, "follows X standard" is sufficient
