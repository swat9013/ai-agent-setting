# Testing Glossary (Khorikov Standards)

## Four Pillars of Good Tests

| Pillar | Description |
|--------|-------------|
| Protection against regressions | Ability to detect bugs. Proportional to code executed |
| Resistance to refactoring | No false positives on implementation changes. **Most important** |
| Fast feedback | Tests execute quickly |
| Maintainability | Tests are easy to understand and modify |

## Observable Behavior vs Implementation Details

| Type | Description | Should Verify? |
|------|-------------|----------------|
| Observable behavior | Public API, final output, externally visible side effects | ✅ |
| Implementation details | Private methods, internal state, call order | ❌ |

**Criteria**: Does it directly contribute to achieving the client's goal?

## Test Doubles

| Type | Role | OK to Verify? |
|------|------|---------------|
| Mock | Emulate outgoing interactions (calls with side effects) | ✅ |
| Stub | Emulate incoming interactions (data retrieval) | ❌ |
| Spy | Hand-written Mock | ✅ |
| Dummy | Values just to satisfy signatures | - |
| Fake | Simplified implementation (in-memory DB, etc.) | - |

**CQS Principle correspondence**:
- Command (has side effects, void return) → Mock
- Query (no side effects, returns value) → Stub

## Dependency Types

| Type | Examples | Test Handling |
|------|----------|---------------|
| Managed dependencies | Application DB | Use real instance |
| Unmanaged dependencies | SMTP, external APIs, message bus | Use Mock |

**Boundary principle**: Do not use mocks to verify communication between internal classes

## Test Styles (Priority Order)

1. **Output-based**: Verify pure function return values ← Least brittle
2. **State-based**: Verify state after operation
3. **Communication-based**: Verify interactions ← Most brittle

## Anti-patterns

| Pattern | Problem |
|---------|---------|
| Structural inspection | Checking internal structure existence. Breaks on refactoring |
| Stub verification | `verify(stub)` couples to implementation details |
| Excessive mocking | Mock all internal collaborators |
| Coverage goals | High coverage doesn't guarantee quality |
