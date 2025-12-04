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
- [ ] レイヤー分離の遵守
- [ ] 依存の方向が正しい（上位→下位のみ）
- [ ] 循環依存がない

### エラーハンドリング
- [ ] 例外の適切な捕捉と処理
- [ ] エラーメッセージが有用
- [ ] リトライロジック（外部連携）

## 🟡 Medium: 改善推奨

### 構造設計（KISS/DRY/SLAP/SRP）
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
