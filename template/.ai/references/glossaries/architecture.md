# アーキテクチャ リファレンス

## レイヤーアーキテクチャ

> **注**: 以下は一般的な例。レビュー時はプロジェクト固有のレイヤー定義（context.md等）を確認すること。

### 典型的なレイヤー構成（クリーンアーキテクチャ）

| レイヤー | 責務 | 例 |
|----------|------|-----|
| **Presentation** | UI、API エンドポイント | Controller, View |
| **Application** | ユースケース、オーケストレーション | Service, UseCase |
| **Domain** | ビジネスルール | Entity, ValueObject, DomainService |
| **Infrastructure** | 外部システム連携 | Repository実装, 外部API Client |

### 依存の方向

```
Presentation → Application → Domain ← Infrastructure
                              ↑
                         依存の中心
```

**原則**: 外側から内側へのみ依存。Domain は何にも依存しない。

| 依存方向 | 可否 | 理由 |
|----------|------|------|
| Controller → Service | ✅ | 外→内 |
| Service → Entity | ✅ | 外→内 |
| Entity → Repository | ❌ | 内→外（インターフェースで逆転） |
| Service → DB Client | ❌ | Application → Infrastructure |

## 境界の種類

| 境界 | 定義 | 越える際のルール |
|------|------|------------------|
| **モジュール境界** | 同一パッケージ内の論理的分離 | 名前のコナーセンス（CoN）で十分 |
| **パッケージ境界** | import/exportで分離 | インターフェース経由を推奨 |
| **レイヤー境界** | アーキテクチャ上の層の分離 | 依存逆転、データ結合を徹底 |
| **サービス境界** | プロセス/ネットワーク越え | API契約、冪等性が必須 |

**原則**: 境界が遠いほど弱い結合形式を使う

---

## 契約による設計と信頼境界線

**原則**: 防御的プログラミングは境界にのみ適用し、内部では契約を信頼する

### 信頼境界線の例

| 境界 | 検証内容 | 信頼できる側 |
|------|----------|-------------|
| HTTP API | リクエストボディ、パラメータ | アプリケーション内部 |
| DB層 | - | DBから取得したデータ（スキーマで保証） |
| 外部API呼び出し | レスポンス形式、ステータス | - |
| モジュール境界 | 公開APIの引数（必要に応じて） | モジュール内部 |

### コード例

```typescript
// ❌ 過剰な防御的プログラミング（内部でも毎回検証）
class OrderService {
  calculateTotal(order: Order): Money {
    if (!order) throw new Error('Order is required');           // 内部でも検証
    if (!order.items) throw new Error('Items required');        // 冗長
    if (order.items.length === 0) throw new Error('Empty');     // 冗長
    return order.items.reduce((sum, item) => sum.add(item.price), Money.zero());
  }
}

// ✅ 信頼境界線での検証 + 内部は契約を信頼
// 境界層（Controller/API Gateway）
class OrderController {
  createOrder(input: unknown): Order {
    const validated = OrderSchema.parse(input);  // 境界で厳密に検証
    return this.orderService.create(validated);  // 検証済みデータを渡す
  }
}

// 内部層（Domain Service）- 契約を信頼
class OrderService {
  calculateTotal(order: Order): Money {  // Order型 = 検証済みの契約
    return order.items.reduce((sum, item) => sum.add(item.price), Money.zero());
  }
}
```
