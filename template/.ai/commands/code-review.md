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

#### A) Task tool対応ツール（Claude Code等）

**必須**: 5つのTask toolを**単一メッセージで並列実行**

⚠️ 自分で直接レビューしない。必ずsub-agentに委譲する。

```
Task(subagent_type="general-purpose", prompt="[セキュリティレビュアー]...")
Task(subagent_type="general-purpose", prompt="[信頼性レビュアー]...")
Task(subagent_type="general-purpose", prompt="[パフォーマンスレビュアー]...")
Task(subagent_type="general-purpose", prompt="[アーキテクチャレビュアー]...")
Task(subagent_type="general-purpose", prompt="[品質レビュアー]...")
```

各promptの構造:
```
あなたは${観点}専門のコードレビュアーです。

原則:
${guides/code-review-agents.mdから該当ロールをコピー}

## チェックリスト
${checklists/code-review/${観点}.mdの内容}

## レビュー対象
${対象コード}

## ドメイン知識
${context.mdから抽出した制約}

## 出力
templates/code-review-output.md に従い、担当観点のみ報告
```

#### B) Task tool非対応ツール（Cursor等）

5観点を**順番に**レビュー（観点ごとにロール切替）:

1. **security** → チェックリスト確認 → 指摘記録
2. **reliability** → チェックリスト確認 → 指摘記録
3. **performance** → チェックリスト確認 → 指摘記録
4. **architecture** → チェックリスト確認 → 指摘記録
5. **quality** → チェックリスト確認 → 指摘記録

各観点で `guides/code-review-agents.md` のロール定義を参照し、その観点の視点でレビューすること。

#### 共通ルール

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
- [ ] レビュー実行方法（以下いずれか）:
  - [ ] Task tool対応: 5つのTask toolを並列実行した（自分でレビューしていない）
  - [ ] Task tool非対応: 5観点を順番にレビューした（各観点でロール切替）
- [ ] 各指摘の行番号が正確
- [ ] 各指摘に観点情報を付与
- [ ] 自己検証で重複・過剰指摘を除外
- [ ] 参照ドキュメント一覧を記載

## 関連

- `/review-update` - レビューの学びを反映
