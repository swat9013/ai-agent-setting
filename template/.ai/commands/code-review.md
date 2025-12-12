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

## 使用方法

```bash
/code-review path/to/file.ts       # 特定ファイル
/code-review src/features/         # ディレクトリ
/code-review feature/branch-name   # ブランチ差分
/code-review                       # 現在のブランチ差分 or ステージング変更
```

## 前提条件

1. レビュー対象ファイルが存在
2. `.ai/context.md` が読み込み可能
3. `.ai/references/checklists/code-review/` が存在

## 実行手順

### 1. 対象特定
- 大規模変更（50ファイル超 or 1000行超）→ Critical/High先行レビューを提案

### 2. ドメイン知識収集
- context.md、docs/ から制約・ドメイン知識を確認

### 3. 自動チェック
- テスト、Lint、ビルド実行。**失敗時は中止**

### 4. レビュー実行

5観点のチェックリストでレビュー:

| 観点 | チェックリスト |
|------|--------------|
| security | `checklists/code-review/security.md` |
| reliability | `checklists/code-review/reliability.md` |
| performance | `checklists/code-review/performance.md` |
| architecture | `checklists/code-review/architecture.md` |
| quality | `checklists/code-review/quality.md` |

→ ロール定義: `guides/code-review-agents.md`

**sub-agent対応ツール**: 5観点を並列実行
**非対応ツール**: シーケンシャル実行

- 設計判断の妥当性を評価
- 一般的パターンからの逸脱は選択肢を提示
- 不明点は `[NEEDS CLARIFICATION: 質問]` を挿入（最大3箇所）

### 5. 結果統合（並列実行時）
- 優先度順（Critical→High→Medium→Low）に再編成
- 同一箇所への指摘は統合、重複排除

### 6. 自己検証
→ `guides/code-review-self-reflection.md`

### 7. 結果出力
→ `templates/code-review-output.md`

## 成功基準

1. 優先度別に整理
2. 確信度・根拠・修正案を含む
3. 自動チェック通過
4. 自己検証実施済み

## 完了チェックリスト

- [ ] 前提条件を満たした
- [ ] 自動チェック実行
- [ ] 5観点のチェックリスト確認
- [ ] 各指摘の行番号が正確
- [ ] 各指摘に観点情報を付与
- [ ] 自己検証で重複・過剰指摘を除外
- [ ] 参照ドキュメント一覧を記載

## 関連

- `/review-update` - レビューの学びを反映
