# Architecture Reference

## Layered Architecture

> **Note**: The following is a general example. When reviewing, check project-specific layer definitions (context.md, etc.).

### Typical Layer Structure (Clean Architecture)

| Layer | Responsibility | Examples |
|-------|---------------|----------|
| **Presentation** | UI, API endpoints | Controller, View |
| **Application** | Use cases, orchestration | Service, UseCase |
| **Domain** | Business rules | Entity, ValueObject, DomainService |
| **Infrastructure** | External system integration | Repository impl, External API Client |

### Dependency Direction

```
Presentation → Application → Domain ← Infrastructure
                              ↑
                       Dependency center
```

**Principle**: Depend only from outer to inner. Domain depends on nothing.

| Dependency Direction | Allowed | Reason |
|---------------------|---------|--------|
| Controller → Service | ✅ | Outer → Inner |
| Service → Entity | ✅ | Outer → Inner |
| Entity → Repository | ❌ | Inner → Outer (invert with interface) |
| Service → DB Client | ❌ | Application → Infrastructure |

## Boundary Types

| Boundary | Definition | Crossing Rules |
|----------|------------|----------------|
| **Module boundary** | Logical separation within same package | Connascence of Name (CoN) sufficient |
| **Package boundary** | Separated by import/export | Interface-mediated recommended |
| **Layer boundary** | Architectural layer separation | Enforce dependency inversion, data coupling |
| **Service boundary** | Cross-process/network | API contracts, idempotency required |

**Principle**: The more distant the boundary, the weaker the coupling should be.

---

## Design by Contract and Trust Boundaries

**Principle**: Apply defensive programming only at boundaries; trust contracts internally.

### Trust Boundary Examples

| Boundary | Validate | Trusted Side |
|----------|----------|--------------|
| HTTP API | Request body, parameters | Application internals |
| DB layer | - | Data from DB (guaranteed by schema) |
| External API call | Response format, status | - |
| Module boundary | Public API arguments (as needed) | Module internals |

### Code Example

```typescript
// ❌ Excessive defensive programming (validation even internally)
class OrderService {
  calculateTotal(order: Order): Money {
    if (!order) throw new Error('Order is required');           // Internal validation
    if (!order.items) throw new Error('Items required');        // Redundant
    if (order.items.length === 0) throw new Error('Empty');     // Redundant
    return order.items.reduce((sum, item) => sum.add(item.price), Money.zero());
  }
}

// ✅ Validation at trust boundary + trust contracts internally
// Boundary layer (Controller/API Gateway)
class OrderController {
  createOrder(input: unknown): Order {
    const validated = OrderSchema.parse(input);  // Strict validation at the boundary
    return this.orderService.create(validated);  // Pass validated data
  }
}

// Internal layer (Domain Service) - trust contracts
class OrderService {
  calculateTotal(order: Order): Money {  // Order type = validated contract
    return order.items.reduce((sum, item) => sum.add(item.price), Money.zero());
  }
}
```
