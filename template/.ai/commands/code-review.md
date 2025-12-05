---
type: command
name: code-review
description: コードレビューを実行し、優先度別フィードバックを提供する
usage:
  - /code-review path/to/file.ts
  - /code-review src/features/
  - /code-review feature/branch-name
  - /code-review
---
# Code Review Command

コードレビューを実行し、優先度別フィードバックを提供する。

## 使用方法

```bash
/code-review path/to/file.ts       # 特定ファイル
/code-review src/features/         # ディレクトリ
/code-review feature/branch-name   # 特定ブランチと main/master との差分
/code-review                       # 引数なし（下記参照）
```

引数なしの場合:
- main/master 以外 → 現在のブランチと main/master との差分
- main/master → ステージング済み・未ステージングの変更

## 前提条件

以下を確認してから実行。満たさない場合は中止し理由を報告:

1. レビュー対象のファイルが存在する
2. `.ai/context.md` が読み込み可能
3. `.ai/references/checklists/code-review.md` が存在する

## 実行手順

### 1. 対象特定
- 引数がファイル/ディレクトリ → そのパスを対象
- 引数がブランチ名 → main/master との差分を取得
- 引数なし → 現在のブランチを判定し上記ルールに従う

### 2. ドメイン知識収集
- context.md の制約・クリティカル領域を確認
- docs/ からドメイン知識を収集（存在する場合）
- 重要ドメイン（決済、認証等）を特定

### 3. 自動チェック実行
- テスト、Lint、ビルドを実行
- **失敗時は修正を促し、レビューを中止**
- 通過後にレビュー開始

### 4. レビュー実行
- `.ai/references/checklists/code-review.md` を読み込む
- Critical → High → Medium → Low の順でチェック
- 重要ドメインは厳格チェック（下記参照）

### 5. 結果出力
- 下記の出力形式に従って報告

## 出力形式

```markdown
# コードレビュー結果: [対象]

## Critical
- [ ] `file.ts:42` [問題] → [修正案]

## High / Medium / Low
...

## 総評
指摘: Critical X, High X, Medium X, Low X
次のアクション: [推奨事項]
```

## 重要ドメイン特別ルール

context.md や docs/ で定義された重要ドメイン配下のコードには以下を厳格に適用:

- **冪等性**: 同じリクエストを2回送っても安全
- **トランザクション管理**: 複数更新はアトミック
- **高テストカバレッジ**: 重要ロジックは全パターン網羅
- **エラーハンドリング**: タイムアウト、ネットワークエラー等を明示的に処理

## 完了チェックリスト

結果報告前に以下をすべて確認。未達成項目があれば修正してから報告:

- [ ] 前提条件をすべて満たした
- [ ] 自動チェック（テスト、Lint、ビルド）を実行した
- [ ] チェックリストの全項目を確認した
- [ ] 各指摘に具体的な修正案と根拠を記載した
- [ ] 優先度（Critical/High/Medium/Low）が適切
- [ ] 出力形式に従っている

## 原則

- 優先順位を明確に、具体的な修正案と根拠を提示
- 曖昧な指摘、主観の押し付け、Lint自動化可能な指摘は避ける

## 関連

- `/review-update` - レビューの学びをチェックリスト・コマンドに反映
