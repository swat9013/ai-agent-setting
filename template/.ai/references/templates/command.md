# Command Creation Template

Template for creating new commands.

## Structure

```markdown
---
type: command
name: command-name
description: Purpose of the command in one line
usage:
  - /command-name arg1
  - /command-name arg2
---
# Command Name

Brief explanation of command purpose.

## Usage

\`\`\`bash
/command-name arg1   # description
/command-name arg2   # description
\`\`\`

## Prerequisites

Verify the following before execution. Abort and report reason if not met:

1. [Required prerequisite 1]
2. [Required prerequisite 2]

## Execution Steps

### 1. [Step name]
- Specific action
- Insert `[NEEDS CLARIFICATION: question]` for unclear points (max 3)

### 2. [Step name]
- Specific action

### 3. Output Results
- Report following the output format below

## Output Format

\`\`\`markdown
# [Title]

## [Section]
[Content]
\`\`\`


## Success Criteria

This command execution is considered successful when:

1. [Specific and verifiable criterion 1]
2. [Specific and verifiable criterion 2]

## Completion Checklist

Verify all items before reporting. Fix any incomplete items before reporting:

- [ ] All prerequisites met
- [ ] [Command-specific check item]
- [ ] Output format followed

## Principles

- [Principles/notes for this command]
```

## Required Elements

| Element | Purpose |
|---------|---------|
| YAML frontmatter | Metadata (name, description, usage) |
| Prerequisites | Pre-execution validation, abort on failure |
| Numbered execution steps | Clear ordering, reliable execution |
| Output format | Consistent result reporting |
| Success criteria | Explicit goals, eliminate ambiguity |
| Completion checklist | Self-verification, quality assurance |

## Design Principles

### Prerequisites
- List minimum conditions required for execution
- **Abort** and report reason if not met (don't silently continue)

### Execution Steps
- Use numbered steps for clear ordering
- Each step includes specific actions
- Use `[NEEDS CLARIFICATION: question]` for ambiguous cases (max 3)

### Success Criteria
- Explicitly state "what must be achieved" from user perspective
- Write in specific, verifiable terms (avoid vague expressions)
- Difference from checklist: Success criteria = **results**, Checklist = **process**

### Completion Checklist
- Self-verification before reporting (like unit tests for your work)
- **Fix incomplete items before reporting**
- Retry up to 3 times; warn user if still unresolved

## Example: Bad vs Good

### Bad: Vague instructions
```markdown
## Steps
- Review the code
- Report if there are problems
```

### Good: Specific instructions
```markdown
## Prerequisites
Verify the following before execution. Abort and report reason if not met:
1. Target file exists
2. `.ai/context.md` is readable

## Execution Steps
### 1. Identify Target
- If argument is file path → that file is the target
- If no argument → current branch diff is the target

### 2. Code Review
- Check naming convention compliance
- Check error handling appropriateness

## Completion Checklist
- [ ] All prerequisites met
- [ ] Each issue includes specific fix suggestion
```
