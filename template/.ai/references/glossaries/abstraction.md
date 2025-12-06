# Abstraction Level Reference

## SLAP (Single Level of Abstraction Principle)

**Definition**: Keep all code within a single function at the same abstraction level.

## Abstraction Level Criteria

| Level | Characteristics | Examples |
|-------|-----------------|----------|
| **High** | Expresses "what to do" | validateOrder(), sendNotification() |
| **Medium** | Business rule implementation | if (order.total > limit), items.filter() |
| **Low** | Technical details | db.query(), JSON.parse(), for loops |

## Violation Example and Fix

```typescript
// ❌ Mixed abstraction levels
async function processOrder(orderId: string) {
  // High: what to do
  const order = await getOrder(orderId);

  // Low: technical details leak in
  const conn = await pool.getConnection();
  try {
    await conn.beginTransaction();
    await conn.query('UPDATE orders SET status = ?', ['processing']);
    await conn.commit();
  } finally {
    conn.release();
  }

  // High: what to do
  await notifyCustomer(order);
}

// ✅ Unified at same abstraction level
async function processOrder(orderId: string) {
  const order = await getOrder(orderId);      // High
  await updateStatus(order, 'processing');    // High
  await notifyCustomer(order);                // High
}

async function updateStatus(order: Order, status: string) {
  // Low-level details consolidated here
  const conn = await pool.getConnection();
  // ...
}
```

## Judgment Hints

- **Does the function name reflect its contents?**: SQL inside processOrder feels wrong
- **Can steps be connected with "and then"?**: Same-level operations connect naturally
- **Does a partial change require touching unrelated code?**: If DB changes require business logic edits, the levels are mixed
