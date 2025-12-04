---
type: command
name: review-update
description: コードレビューの学びをチェックリスト・コマンドに反映
usage:
  - /review-update
---

# Review Update Command

コードレビューセッションを振り返り、チェックリスト・コマンドを改善する。

## 対象ファイル

- `.ai/references/checklists/code-review.md` - チェック項目
- `.ai/commands/code-review.md` - レビューフロー

## 手順

### 1. 抽出
セッションから保存すべき内容を特定：
- 新しいチェック観点（セキュリティ、パフォーマンス等）
- 有効だったパターン・アンチパターンの例
- 繰り返し指摘した問題
- レビューフローの改善点

### 2. 整合性チェック
- 既存項目との矛盾・重複がないか確認
- 優先度（Critical/High/Medium/Low）の妥当性確認

### 3. 規模チェック
```bash
python3 .ai/scripts/measure-context.py --references
```
閾値超過時は追記前に圧縮。

### 4. 保存先判断

| 種類 | 保存先 |
|-----|-------|
| チェック項目・パターン例 | .ai/references/checklists/code-review.md |
| レビューフロー・出力形式 | .ai/commands/code-review.md |

### 5. 同期
```bash
python3 .ai/scripts/sync-context.py
```

## 圧縮方針
1. 重複統合（類似チェック項目をまとめる）
2. 表現簡潔化
3. 頻出項目は優先度を上げる
4. 有効でないパターン例は削除

## 出力形式
```
### 変更サマリー
- チェックリスト: 追加X件、修正X件、削除X件
- コマンド: 追加/修正/変更なし
- 圧縮: 実施/不要

### 更新内容
[差分または追加項目]
```

## 原則
- 具体的な修正例（Good/Bad）を重視
- プロジェクト固有すぎる項目は context.md へ
- 汎用的なベストプラクティスをチェックリストへ

## 関連

- `/code-review` - コードレビュー実行
