# Modeling Glossary

Terminology definitions used for modeling suggestions in code reviews.

## Core Principle: High Cohesion, Loose Coupling

**Keep related data and logic together.**

| Location | Data | Logic | Examples |
|----------|------|-------|----------|
| Value Object | Value attributes | Operations/validation on that value | Money.add(), Email.validate() |
| Entity | State | Operations that change state | Order.cancel(), User.changeEmail() |
| Domain Service | None | Operations belonging to neither above | TransferService.execute() |

Domain Service is the last resort for "belongs nowhere." Overuse leads to anemic domain model.

---

## Resource vs Event

| Concept | Definition | Characteristics | Examples |
|---------|------------|-----------------|----------|
| **Resource** | Data representing current system state | Managed via CRUD, updated | User, Order, Product |
| **Event** | Record of past facts | Immutable, append-only, never deleted | OrderPlaced, PaymentReceived |

**Decision criteria**: "Will this data be updated?"
- Yes → Resource
- No (record of fact) → Event

**Caution with update/delete**:
update/delete on resources means "loss of historical facts." Record as events when:
- Audit required (who, when, what changed)
- History reference needed (want to know past states)
- Undo/redo required

**Benefits of separation**:
- Audit log and history completeness
- Path to event sourcing
- Resource schema changes don't affect history

---

## Entity vs Value Object

| Concept | Definition | Identification | Examples |
|---------|------------|----------------|----------|
| **Entity** | Object identified by identity (ID) | Same ID = same object | User(id=1), Order(id=abc) |
| **Value Object** | Object identified by attribute values | Same attributes = same object | Money(100, JPY), Email("a@b.com") |

**Decision criteria**: "Are two instances with same attribute values considered identical?"
- Yes → Value Object
- No (need to treat as different) → Entity

**Value Object characteristics**:
- Immutable: Create new instance on change
- Value equality: Equal if all attributes match
- Self-validating: Validate on creation

**Benefits of VO**:
- Type safety (prevent primitive type misuse)
- Centralized validation logic
- Explicit domain knowledge

---

## Domain Service

| Concept | Definition | Example |
|---------|------------|---------|
| **Domain Service** | Domain logic belonging to neither VO nor Entity | TransferService.execute(from, to, amount) |

**Use cases**:
- Operations spanning multiple aggregates (transfer: source and destination)
- Domain logic for external service integration

**Decision priority**:
1. First consider if it fits in VO
2. Then consider if it fits in Entity
3. Only use Domain Service if it fits neither

---

## Aggregate

| Concept | Definition |
|---------|------------|
| **Aggregate** | Unit of consistency. Access internals only through aggregate root |
| **Aggregate Root** | Entity serving as aggregate entry point. External access goes through this |

**Example**: Order (aggregate root) → OrderLine (internal entity)

**Design guidelines**:
- Keep aggregates small (1 transaction = 1 aggregate update is ideal)
- Inter-aggregate references by ID only (not object references)
