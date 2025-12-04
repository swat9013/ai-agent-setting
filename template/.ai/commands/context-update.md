---
type: command
name: context-update
description: セッションを振り返り、コンテキストファイルを更新する
usage:
  - /context-update
---

# Context Update Command

セッションを振り返り、コンテキストを更新する。

## 前提

- `.ai/context.md` が唯一の真実の源（SSOT）
- `AGENTS.md`, `CLAUDE.md` 等は `sync-context.py` で自動生成される出力
- 編集は必ず `.ai/context.md` に対して行う

## 手順

### 1. 抽出
保存すべき内容を特定：
- 新しく学んだこと、設計判断とその理由、落とし穴
- 3回以上繰り返された説明・指摘・ワークフロー
- コードレビューで繰り返し指摘された問題

### 2. 整合性チェック
- 矛盾・重複・古い情報がないか確認

### 3. 規模チェック
```bash
python3 .ai/scripts/measure-context.py
```
閾値超過時は追記前に圧縮。

### 4. 保存先判断

| 種類 | 保存先 |
|-----|-------|
| プロジェクト全般ルール | .ai/context.md |
| 設計判断（ADR形式） | docs/decisions/ |
| 詳細ガイドライン | docs/guidelines/ |
| 新規エージェント/コマンド | .ai/agents/ or .ai/commands/ |

ADRテンプレート: `.ai/references/templates/adr.md`

エージェント＝対話・相談向け、コマンド＝アクション実行。1:1対応ならコマンドに統合。

### 5. 同期
context.md 更新後は各ツール向けファイルを同期:
```bash
python3 .ai/scripts/sync-context.py
```
同期先: `AGENTS.md`, `CLAUDE.md`, `.cursor/`, `.github/instructions/`, `.claude/`

## 圧縮方針
1. 重複統合  2. 表現簡潔化  3. 詳細は docs/ へ分離  4. 古い情報は削除

## 出力形式
```
### 変更サマリー
- 追加/修正/削除: X件、圧縮: 実施/不要

### 更新内容
[差分または全文]
```

## 原則
- 最小限の高シグナル情報で効果最大化
- 適切な抽象度（硬直的すぎず曖昧すぎず）
- 詳細リンクは分離時のみ追加
- AIが既知の概念は「〜に準拠」で十分
