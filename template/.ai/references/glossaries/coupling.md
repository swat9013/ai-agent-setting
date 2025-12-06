# Coupling and Connascence Reference

## Coupling Types (from weakest to strongest)

| Type | Description | Severity |
|------|-------------|----------|
| **Data coupling** | Pass only primitive data | ✅ Best |
| **Stamp coupling** | Pass composite data structure, use only part | ⚠️ Mild |
| **Control coupling** | Pass control flags to change behavior | ⚠️ Medium |
| **Common coupling** | Share global variables/state | ❌ High |
| **Content coupling** | Directly reference/modify another module's internals | ❌ Worst |

**Directional Metrics**:
- **Afferent coupling**: Number depending on this module → High means wide impact
- **Efferent coupling**: Number this module depends on → High means too many responsibilities

## Connascence

Dependencies where "changing one requires changing the other."

### Static Connascence (from weakest to strongest)

| Type | Description | Example | Improvement |
|------|-------------|---------|-------------|
| **Name (CoN)** | Reference same name | Function names, variable names | Clear intentional naming |
| **Type (CoT)** | Expect same type | Argument types, return types | Shared type definitions |
| **Meaning (CoM)** | Assign meaning to specific values | `status == 1` means active | Extract to enums/constants |
| **Position (CoP)** | Depend on order | Positional args, array indices | Named args, dictionaries/objects |
| **Algorithm (CoA)** | Use same algorithm | Hash, encryption, validation | Single shared implementation |

### Dynamic Connascence (stronger)

| Type | Description | Example | Improvement |
|------|-------------|---------|-------------|
| **Execution (CoE)** | Depend on call order | init()→process()→cleanup() | State machine, builder pattern |
| **Timing (CoTm)** | Depend on execution timing | Race conditions, timeouts | Synchronization, event-driven |
| **Value (CoV)** | Multiple values change together | Same values in test and impl | Indirect reference (constants, config) |
| **Identity (CoI)** | Reference same instance | Shared objects | Explicit dependency injection |

### 3-Axis Evaluation

1. **Strength**: Stronger = harder to refactor
2. **Locality**: More distant = more problematic (within the same file is acceptable)
3. **Degree**: Wider impact = more problematic

## Code Examples

```typescript
// ❌ Connascence of Position (CoP)
function createUser(name: string, email: string, age: number, isAdmin: boolean) {}
createUser("John", "john@example.com", 30, true); // Must remember order

// ✅ Improved to Connascence of Name (CoN)
function createUser(params: { name: string; email: string; age: number; isAdmin: boolean }) {}
createUser({ name: "John", email: "john@example.com", age: 30, isAdmin: true });
```

```typescript
// ❌ Common coupling (global state)
let currentUser: User | null = null;
function processOrder() {
  if (currentUser) { /* ... */ } // Depends on global variable
}

// ✅ Data coupling (explicit argument)
function processOrder(user: User) { /* ... */ }
```
