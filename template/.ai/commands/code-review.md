---
type: command
name: code-review
description: コードレビューを実行し、優先度別フィードバックを提供する
usage:
  - /code-review path/to/file.ts
  - /code-review src/features/
  - /code-review
---
# Code Review Command

コードレビューを実行し、優先度別フィードバックを提供する。

## 使用方法

```bash
/code-review path/to/file.ts  # 特定ファイル
/code-review src/features/    # ディレクトリ
/code-review                  # git diff の変更
```

## 処理フロー

1. 対象特定（引数 or git diff）
2. context.md の制約確認
3. **`.ai/references/checklists/code-review.md` を読み込む**
4. 自動チェック結果確認（テスト、Lint、ビルド）
5. チェックリストに従い Critical → Low の順でレビュー

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

## 原則

- 優先順位を明確に、具体的な修正案と根拠を提示
- 曖昧な指摘、主観の押し付け、Lint自動化可能な指摘は避ける
