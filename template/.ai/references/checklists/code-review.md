# コードレビューチェックリスト

## 🔴 Critical: 即修正必須

### セキュリティ
- [ ] SQLインジェクション対策（パラメータバインディング）
- [ ] XSS対策（サニタイズ、エスケープ）
- [ ] CSRF対策
- [ ] 認証・認可の適切な実装
- [ ] 機密情報のログ出力禁止
- [ ] ハードコードされた認証情報がないこと

### データ整合性
- [ ] 適切な制約（外部キー、NOT NULL、ユニーク）
- [ ] トランザクション管理（複数更新はアトミック）
- [ ] マイグレーションの可逆性（rollback可能）

### 重要ロジック
- [ ] 冪等性の考慮（必要な場合）
- [ ] エラーハンドリングの網羅
- [ ] 境界値・エッジケースの処理

## 🟠 High: 早急に対応

### パフォーマンス
- [ ] N+1クエリの回避
- [ ] 不要なデータ取得の回避（SELECT *禁止）
- [ ] 適切なインデックス
- [ ] ページネーション（大量データ）

### アーキテクチャ

→ 用語定義: `.ai/references/glossaries/architecture.md`

- [ ] レイヤー分離の遵守
- [ ] 依存の方向が正しい（上位→下位のみ）
- [ ] 循環依存がない

### 結合度・コナーセンス

→ 用語定義: `.ai/references/glossaries/coupling.md`、`.ai/references/glossaries/architecture.md`（境界の種類）

- [ ] 強い結合（内容結合・共通結合）がないか
- [ ] 動的コナーセンス（実行順序・タイミング・値・同一性）が最小限か
- [ ] 境界を越える結合は弱い形式（データ結合・名前のコナーセンス）か

### エラーハンドリング
- [ ] 例外の適切な捕捉と処理
- [ ] エラーメッセージが有用
- [ ] リトライロジック（外部連携）

### 契約による設計と信頼境界線

→ 用語定義: `.ai/references/glossaries/architecture.md`（契約による設計、境界の種類）

- [ ] 信頼境界線が明確に定義されている（外部入力、API境界、モジュール境界）
- [ ] 境界上でのみバリデーション・サニタイズを実施（内部では信頼）
- [ ] 事前条件・事後条件・不変条件が適切に定義されている
- [ ] 防御的コードが境界に集中し、内部ロジックは簡潔か

## 🟡 Medium: 改善推奨

### 構造設計（KISS/DRY/SLAP/SRP）

→ 用語定義: `.ai/references/glossaries/abstraction.md`

- [ ] 最もシンプルな解決策になっている
- [ ] 同じ責務を持つコードが一箇所にまとまっている
- [ ] 1関数内が同じ抽象レベルで記述されている
- [ ] 1クラス/モジュールが1つの責任のみ持つ

### 可読性
- [ ] メソッド長が適切（目安: 20行以下）
- [ ] クラス長が適切（目安: 300行以下）
- [ ] ネストが深すぎない（目安: 3レベル以下）
- [ ] 変数名・関数名が明確
- [ ] マジックナンバーの定数化

### テスタビリティ
- [ ] 依存注入が可能な設計
- [ ] モック可能な外部依存
- [ ] 副作用の分離
- [ ] テストが追加されている

### コード品質
- [ ] Lint/静的解析の警告なし
- [ ] 未使用のコード・インポートなし
- [ ] TODO/FIXMEにチケット番号あり

## 🟢 Low: 余力があれば

### モデリング提案（採用は実装者判断）

以下の観点でモデルの分解を提案する。強制ではなく「こう分解できる」という選択肢の提示。

→ 用語定義: `.ai/references/glossaries/modeling.md`

#### リソース vs イベント
- [ ] 更新されるデータ（リソース）と、過去の事実の記録（イベント）が混在していないか
- [ ] イベントとして扱うべきもの（注文履歴、操作ログ等）がリソースとして実装されていないか
- [ ] update/deleteで過去の事実が失われていないか（監査・履歴が必要なデータ）

#### エンティティ vs バリューオブジェクト
- [ ] IDで識別すべきもの（エンティティ）と、値で識別できるもの（VO）が適切に分離されているか
- [ ] 金額、メールアドレス、住所等がプリミティブ型のままになっていないか

#### データとロジックの凝集
- [ ] 関連するデータとロジックが同じ場所にまとまっているか（VO、エンティティ、ドメインサービス）
- [ ] ロジックがサービス層に漏れ出していないか（貧血ドメインモデル）

### ドキュメント
- [ ] 公開APIにコメント/ドキュメント
- [ ] 複雑なロジックに説明コメント
- [ ] READMEの更新（必要な場合）

### 保守性
- [ ] YAGNI原則（必要最小限）
- [ ] 一貫した命名規則
- [ ] 適切なファイル配置

---

## よくあるパターンと修正例

### N+1クエリ

```typescript
// ❌ Bad
const users = await User.findAll();
for (const user of users) {
  const posts = await user.getPosts(); // N回のクエリ
}

// ✅ Good
const users = await User.findAll({
  include: [Post] // 1回のクエリ
});
```

### エラーハンドリング

```typescript
// ❌ Bad
async function fetchData() {
  const response = await fetch(url);
  return response.json();
}

// ✅ Good
async function fetchData() {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }
  return response.json();
}
```

### 依存注入

```typescript
// ❌ Bad
class UserService {
  private db = new Database(); // 直接生成
}

// ✅ Good
class UserService {
  constructor(private db: Database) {} // 注入
}
```

### バリューオブジェクトの抽出

```typescript
// ❌ プリミティブ型のまま
class Order {
  constructor(
    public id: string,
    public amount: number,      // 金額なのに number
    public currency: string,    // 通貨が別管理
    public email: string        // バリデーションがバラバラ
  ) {}
}

// ✅ VOとして抽出
class Money {
  constructor(
    public readonly amount: number,
    public readonly currency: Currency
  ) {
    if (amount < 0) throw new Error('Amount must be non-negative');
  }
  add(other: Money): Money { /* ... */ }
}

class Email {
  constructor(public readonly value: string) {
    if (!this.isValid(value)) throw new Error('Invalid email');
  }
  private isValid(email: string): boolean { /* ... */ }
}
```

### リソース vs イベントの分離

```typescript
// ❌ リソースとイベントが混在
class Order {
  status: string;           // リソース（現在状態）
  statusHistory: string[];  // イベント（履歴）← 同じテーブルに混在
}

// ✅ 分離
class Order {                          // リソース: 現在状態
  status: OrderStatus;
}
class OrderStatusChanged {             // イベント: 不変の事実
  readonly orderId: string;
  readonly from: OrderStatus;
  readonly to: OrderStatus;
  readonly changedAt: Date;
}
```

