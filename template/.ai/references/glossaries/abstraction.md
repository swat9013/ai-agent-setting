# 抽象レベル リファレンス

## SLAP（Single Level of Abstraction Principle）

**定義**: 1つの関数内では、同じ抽象度の処理のみを記述する

## 抽象レベルの判断基準

| レベル | 特徴 | 例 |
|--------|------|-----|
| **高** | 「何をするか」を表現 | validateOrder(), sendNotification() |
| **中** | ビジネスルールの実装 | if (order.total > limit), items.filter() |
| **低** | 技術的詳細 | db.query(), JSON.parse(), for loops |

## 違反例と修正

```typescript
// ❌ 抽象レベル混在
async function processOrder(orderId: string) {
  // 高: 何をするか
  const order = await getOrder(orderId);

  // 低: 技術的詳細が混入
  const conn = await pool.getConnection();
  try {
    await conn.beginTransaction();
    await conn.query('UPDATE orders SET status = ?', ['processing']);
    await conn.commit();
  } finally {
    conn.release();
  }

  // 高: 何をするか
  await notifyCustomer(order);
}

// ✅ 同じ抽象レベルで統一
async function processOrder(orderId: string) {
  const order = await getOrder(orderId);      // 高
  await updateStatus(order, 'processing');    // 高
  await notifyCustomer(order);                // 高
}

async function updateStatus(order: Order, status: string) {
  // 低レベルの詳細はここに集約
  const conn = await pool.getConnection();
  // ...
}
```

## 判断のヒント

- **関数名と中身が合っているか？**: processOrder の中に SQL があれば違和感
- **説明するとき「そして」で繋げられるか？**: 同じレベルなら自然に繋がる
- **一部だけ変更が必要になるか？**: DB変更時にビジネスロジックまで触るなら混在の兆候
