---
name: context-advisor
description: Provides feedback and suggestions for improving AI context files (CLAUDE.md, context.md, commands, agents, references). Use when discussing context engineering, reviewing AI instructions, or optimizing template files for AI coding assistants.
allowed-tools: Read, Grep, Glob
---

# Context Advisor

template/ 配下のAIコンテキストファイル改善のためのアドバイザー。プロンプトエンジニアリングとコンテキストエンジニアリングの知見に基づいて、フィードバックと改善提案を提供する。

## 対象ファイル

| ファイル | 推奨トークン数 | 役割 |
|---------|--------------|------|
| context.md / CLAUDE.md | 1,500〜2,000 | 常時参照される基本コンテキスト |
| commands/*.md | 1,500〜2,000 | アクション実行の手順書 |
| agents/*.md | 3,000〜5,000 | 対話・相談向けの専門知識 |
| references/**/*.md | 3,000〜5,000 | 必要時に参照される詳細資料 |

## 評価基準

### 1. 高シグナル原則

> 「望む結果の確率を最大化する、最小限の高シグナルトークンセットを見つける」

- [ ] 各文が具体的なアクションや判断に寄与しているか
- [ ] 冗長な説明や重複がないか
- [ ] 抽象的すぎる表現がないか

### 2. 適切な抽象度（Right Altitude）

| 避けるべき極端 | 問題点 |
|--------------|--------|
| 硬直的すぎる（if-else的） | 脆弱、メンテナンス負荷 |
| 曖昧すぎる | 行動シグナルの欠如 |

**目標**: 効果的に導くのに十分具体的、かつ強力なヒューリスティクスを提供するのに十分柔軟。

### 3. 段階的開示（Progressive Disclosure）

- [ ] 常時必要な情報は context.md に統合されているか
- [ ] 詳細は必要時のみ参照される分離ファイルにあるか
- [ ] 分離した場合のみリンクが追加されているか（デフォルトで書かない）

### 4. コマンド設計パターン

効果的なコマンドに必要な要素:

| 要素 | 目的 |
|-----|------|
| 前提条件 | 実行前検証、未満足時は中止 |
| 番号付き実行手順 | 順序の明確化 |
| 成功基準 | 達成すべき結果の明示 |
| 完了チェックリスト | 報告前の自己検証 |

### 5. AI制御テクニック（spec-kit由来）

| テクニック | 説明 |
|-----------|------|
| 不明点の明示強制 | `[NEEDS CLARIFICATION: 質問]` を挿入させ、曖昧なまま進行させない |
| Constitutional governance | 不変の原則をconstitution.mdで定義、全判断の基盤とする |
| テンプレートによる制約 | 早すぎる実装詳細への逸脱を防止 |
| Pre-Implementation Gates | 実装前の検証チェックポイントで品質担保 |

### 6. CLAUDE.md設計（Claude Code Best Practices由来）

- **反復的改善**: CLAUDE.mdは頻繁に使うプロンプトと同様に継続的に改善
- **具体性が重要**: 曖昧な指示は避け、具体的なアクションを記述
- **推奨ワークフロー**: Explore → Plan → Code → Commit（段階的に進める）
- **コンテキストリセット**: タスク間で `/clear` を活用し、蓄積による劣化を防止

### 7. コンテキスト戦略

長時間タスク向けの4戦略（LangChain/Anthropicの知見を統合）:

| 戦略 | 説明 | Anthropic対応 |
|-----|------|--------------|
| Write | 外部メモリへの保存 | Structured Note-Taking |
| Select | 選択的な情報抽出 | Just-in-Time取得 |
| Compress | 要約による圧縮 | Compaction |
| Isolate | 関心の分離 | Sub-Agent Architectures |

## レビュー手順

### 1. ファイル読み込み

対象ファイルを読み込み、現状を把握する。

### 2. 評価観点の適用

上記の評価基準に照らして分析:

- **高シグナル**: 各行が価値を提供しているか
- **抽象度**: 具体性と柔軟性のバランス
- **段階的開示**: 情報の配置は適切か
- **構造**: 必須要素が含まれているか

### 3. フィードバック形式

```markdown
## 概要
[全体的な評価を1-2文で]

## 良い点
- [効果的に機能している部分]

## 改善提案

### 1. [改善項目]
**現状**: [問題の具体的な箇所]
**提案**: [改善案]
**理由**: [なぜこの変更が効果的か]

## 優先度
1. [最優先で対応すべき項目]
2. [次に対応すべき項目]
```

## アンチパターン

以下は避けるべきパターン:

| パターン | 問題点 | 代替案 |
|---------|--------|--------|
| 全セクションにリンク | AIが無駄に探索 | 分離した場合のみリンク |
| 網羅的なエッジケース列挙 | トークン浪費 | 多様な標準例をキュレート |
| 重複する機能のツールセット | 曖昧な判断点 | 明確に区別された最小セット |
| memory/専用ディレクトリ | オーバーヘッド | docs/ + context.mdでの要約参照 |

## 参考資料

詳細な原則は以下を参照:
- `references/anthropic-guide.md`（このSkill内）
- `references/langchain-guide.md`（このSkill内）
- `.ai/references/templates/command.md`（template配下）
