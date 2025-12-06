# ADR (Architecture Decision Record) Template

Template for documenting architectural decisions.

## When to Use

- When making architecture-impacting decisions
- When choosing one option from multiple alternatives
- When future explanation of "why this is so" will be needed

## Template

```markdown
# ADR-[number]: [Title]

## Status

[Proposed | Accepted | Deprecated | Superseded by ADR-XXX]

## Context

### Background
[What situation required this decision]

### Constraints
- [Technical constraints]
- [Business constraints]
- [Deadlines, etc.]

### Options Considered

**Option A: [name]**
- Overview: [description]
- Pros: [advantages]
- Cons: [disadvantages]

**Option B: [name]**
- Overview: [description]
- Pros: [advantages]
- Cons: [disadvantages]

## Decision

### Adopted Design
[The chosen design]

### Rationale
1. [Reason 1]
2. [Reason 2]
3. [Reason 3]

## Consequences

### Positive
- [Positive impact 1]
- [Positive impact 2]

### Negative
- [Negative impact 1]
- [Negative impact 2]

### Mitigation
- [Mitigation strategy 1]
- [Mitigation strategy 2]

## Notes

### Related Documents
- [Links to related ADRs or documents]

### Decision Date
[YYYY-MM-DD]
```

## Save Location

`docs/decisions/ADR-[number]-[slug].md`

Example: `docs/decisions/ADR-001-use-typescript.md`

## Naming Convention

- Number: Sequential (001, 002, ...)
- Slug: Short description in kebab-case

## Status Meanings

| Status | Meaning |
|--------|---------|
| Proposed | Under review |
| Accepted | Approved (ready for implementation) |
| Deprecated | Not recommended for new use |
| Superseded | Replaced (refer to new ADR) |
