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

### 1. 対象特定と規模判定
- 引数に応じてレビュー対象を特定
- 大規模変更（50ファイル超 or 1000行超）→ Critical/High のみ先行レビューを提案

### 2. ドメイン知識収集
- context.md の制約・クリティカル領域を確認
- docs/ からドメイン知識を収集（存在する場合）

### 3. 自動チェック実行
- テスト、Lint、ビルドを実行
- **失敗時は修正を促し、レビューを中止**

### 4. レビュー実行
- `.ai/references/checklists/code-review.md` を読み込む
- チェックリスト内の「→ 用語定義:」リンク先をすべて読み込む
- Critical → High → Medium → Low の順でチェック
- MR説明の背景情報（調査結果、実行計画等）を活用し、設計判断の妥当性を評価
- 一般的パターンからの逸脱は選択肢を提示（現状維持推奨でも却下案を明記）
- 不明点は `[NEEDS CLARIFICATION: 質問]` を挿入（最大3箇所）

### 5. 自己検証

→ 詳細: `.ai/references/guides/code-review-self-reflection.md`

各指摘を位置検証・構文検証・コンテキスト整合・重複排除・過剰指摘フィルタで再検証。

### 6. 結果出力

→ テンプレート: `.ai/references/templates/code-review-output.md`

## 重要ドメイン特別ルール

context.md で定義された重要ドメイン配下は以下を厳格に適用:
- 冪等性、トランザクション管理、高テストカバレッジ、エラーハンドリング

## 成功基準

1. 問題点が優先度別（Critical/High/Medium/Low）に整理されている
2. 各指摘に確信度スコア・根拠・具体的な修正案が含まれている
3. 自動チェック（テスト、Lint、ビルド）が通過している
4. 自己検証を実施し、不正確な指摘を除外済み

## 完了チェックリスト

- [ ] 前提条件をすべて満たした
- [ ] 自動チェックを実行した
- [ ] チェックリストの全項目を確認した
- [ ] 用語定義リンク先をすべて読み込んだ
- [ ] 各指摘の行番号が正確
- [ ] 自己検証で重複・過剰指摘を除外した
- [ ] 大規模変更の場合、段階的レビューを提案した
- [ ] 優先度（Critical/High/Medium/Low）が適切
- [ ] 参照したドキュメント一覧を記載した

## 原則

- 優先順位を明確に、具体的な修正案と根拠を提示
- 曖昧な指摘、主観の押し付け、Lint自動化可能な指摘は避ける

## 関連

- `/review-update` - レビューの学びをチェックリスト・コマンドに反映
