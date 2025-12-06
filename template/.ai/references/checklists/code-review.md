# Code Review Checklist

> Warning: Refer to "→ Definition:" links in each section for evaluation criteria

## Critical: Immediate Fix Required

### Security
- [ ] SQL injection prevention (parameter binding)
- [ ] XSS prevention (sanitization, escaping)
- [ ] CSRF protection
- [ ] Proper authentication/authorization implementation
- [ ] No sensitive information in logs
- [ ] No hardcoded credentials

### Data Integrity
- [ ] Proper constraints (foreign keys, NOT NULL, unique)
- [ ] Transaction management (atomic multi-updates)
- [ ] Migration reversibility (rollback possible)

### Critical Logic
- [ ] Idempotency considered (when required)
- [ ] Comprehensive error handling
- [ ] Boundary/edge case handling

## High: Address Promptly

### Performance
- [ ] N+1 query prevention
- [ ] Avoid unnecessary data fetching (no SELECT *)
- [ ] Proper indexing
- [ ] Pagination (for large data)
- [ ] Verify execution plan for complex queries (OR joins, EXISTS subqueries)

### Architecture

→ Definition: `.ai/references/glossaries/architecture.md`

- [ ] Layer separation compliance
- [ ] Correct dependency direction (upper → lower only)
- [ ] No circular dependencies

### Coupling and Connascence

→ Definition: `.ai/references/glossaries/coupling.md`, `.ai/references/glossaries/architecture.md` (boundary types)

- [ ] No strong coupling (content/common coupling)
- [ ] Dynamic connascence (execution order, timing, value, identity) minimized
- [ ] Cross-boundary coupling uses weak forms (data coupling, connascence of name)

### Error Handling
- [ ] Proper exception catching and handling
- [ ] Useful error messages
- [ ] Retry logic (for external integrations)

### Design by Contract and Trust Boundaries

→ Definition: `.ai/references/glossaries/architecture.md` (design by contract, boundary types)

- [ ] Trust boundaries clearly defined (external input, API boundaries, module boundaries)
- [ ] Validation/sanitization only at boundaries (trust internally)
- [ ] Preconditions, postconditions, invariants properly defined
- [ ] Defensive code concentrated at boundaries; internal logic kept simple

## Medium: Improvement Recommended

### Design Decisions (Trade-offs)
- [ ] If deviating from common optimization patterns, verify it's intentional

### Structural Design (KISS/DRY/SLAP/SRP)

→ Definition: `.ai/references/glossaries/abstraction.md`

- [ ] Simplest solution chosen
- [ ] Code with same responsibility consolidated in one place
- [ ] Same abstraction level within each function
- [ ] Each class/module has single responsibility

### Readability
- [ ] Appropriate method length (guideline: 20 lines or less)
- [ ] Appropriate class length (guideline: 300 lines or less)
- [ ] Nesting not too deep (guideline: 3 levels or less)
- [ ] Clear variable/function names
- [ ] Magic numbers extracted to constants

### Test Quality (Khorikov 4 Pillars)

→ Definition: `.ai/references/glossaries/testing.md`

- [ ] Verifying observable behavior (not implementation details)
- [ ] Resistant to refactoring (won't break on legitimate refactoring)
- [ ] Mocks used only at boundaries (unmanaged dependencies)
- [ ] Not verifying stub calls (no verify on stubs)
- [ ] Tests tied to business requirements

### Code Quality
- [ ] No lint/static analysis warnings
- [ ] No unused code/imports
- [ ] TODOs/FIXMEs have ticket numbers

## Low: If Time Permits

### Modeling Suggestions (Adoption at Implementer's Discretion)

Suggest model decomposition from these perspectives. Not mandatory—just presenting alternatives.

→ Definition: `.ai/references/glossaries/modeling.md`

#### Resource vs Event
- [ ] Current state data (resources) and historical records (events) are properly separated
- [ ] Data that should be events (order history, operation logs) is not incorrectly implemented as resources
- [ ] Updates/deletes preserve historical facts when audit trails or history are required

#### Entity vs Value Object
- [ ] Proper separation of ID-identified (entity) and value-identified (VO) objects
- [ ] Amounts, email addresses, and addresses are not left as primitive types

#### Data and Logic Cohesion
- [ ] Related data and logic consolidated (VO, entity, domain service)
- [ ] Logic doesn't leak to service layer (avoiding anemic domain model)

### Comments

What to write for each target:
- Code → How / Test code → What / Commit log → Why / Comments → **Why not**

- [ ] Consider whether better naming could replace the comment
- [ ] "Why not" (why another approach wasn't chosen) is explained
- [ ] Comments match the code (no stale comments)
- [ ] Comments are not redundant (not repeating the obvious)
- [ ] No commented-out code (should be in Git)
- [ ] Public APIs have doc comments

### Maintainability
- [ ] YAGNI principle (minimum necessary)
- [ ] Consistent naming conventions
- [ ] Appropriate file placement

---

## Common Patterns and Fixes

### N+1 Query

```typescript
// ❌ Query inside loop
for (const user of users) { await user.getPosts(); }
// ✅ Eager Loading
const users = await User.findAll({ include: [Post] });
```

### Error Handling

```typescript
// ❌ No response check
return response.json();
// ✅ Status verification
if (!response.ok) throw new Error(`HTTP ${response.status}`);
```

### Dependency Injection, VO, Resource Separation

```typescript
// ❌ Direct dependency creation
class UserService { private db = new Database(); }
// ✅ Constructor injection
class UserService { constructor(private db: Database) {} }

// ❌ Primitive types: amount: number; email: string;
// ✅ Extracted as VO: Money, Email (with built-in validation)

// ❌ Mixed: status + statusHistory[] in same entity
// ✅ Separated: Order (current state) + OrderStatusChanged (history event)
```

### Tests: Mock/Stub and Implementation Detail Verification

```typescript
// ❌ Verifying stub calls (coupling to implementation details)
verify(userRepo.findById).toHaveBeenCalledWith(id);

// ❌ Spying on internal methods (breaks on refactoring)
expect(jest.spyOn(service, 'calculateDiscount')).toHaveBeenCalled();

// ✅ Verify only final results
expect(result).toEqual(expectedUser);
expect(result.total).toBe(900);
```

### Comments

```typescript
// ❌ Explaining How: x = x + 1; // add 1 to x
// ❌ Solvable by naming: const d = 7; // retention days
// ✅ Express in naming: const retentionDays = 7;
// ✅ Why not: // Using loop (recursion risks stack overflow)
```

### Design Decisions (Trade-off) Presentation

```ruby
# Common pattern (1 query)
titles = Title.bookmarked_by(user_id).current

# Intentional separation (2 queries) - to avoid SQL optimizer issues
bookmarked_ids = Title.bookmarked_by(user_id).pluck(:id)
current_ids = Title.where(id: bookmarked_ids).current.pluck(:id)
```

Review handling:
- MR description explains separation → Recommend current approach + present merge option
- Reason unclear → Present merge option and confirm intent

### Complex Query Execution Plans

Complex queries (OR joins, EXISTS subqueries) may not get expected execution plans from SQL optimizer.

```ruby
# Note: Complex queries require execution plan verification
titles = Title.where(...).or(Title.where(...))
# → Verify with EXPLAIN ANALYZE on production-like data
```

**Cases requiring verification**:
- Scope uses `or()`
- Scope contains `EXISTS` subquery
- May handle large data volumes

**Countermeasures**:
- Verify expected execution plan with `EXPLAIN ANALYZE` on production-like data
- If issues found, consider query separation or index additions
