# コンテキスト育成システム 設計書

*Context Growing System Design Document*

---

## 1. 概要

本システムは、AIコーディングアシスタント（Cursor、Claude Code、GitHub Copilot等）との対話を通じて蓄積される知識・コンテキストを効率的に管理・成長させるための仕組みを提供する。

会話から得られた指摘やノウハウを体系的に保存し、プロジェクトの成長とともにコンテキストも進化させることを目的とする。

### 対応ツール

| ツール | コンテキストファイル | コマンド機能 |
|--------|---------------------|--------------|
| Cursor | `.cursorrules`, `.cursor/rules/` | ✅ カスタムコマンド |
| GitHub Copilot | `.github/copilot-instructions.md` | ✅ スラッシュコマンド |
| Claude Code | `CLAUDE.md`, `AGENTS.md` | ✅ カスタムコマンド |
| Codex CLI | `AGENTS.md`, プロジェクトドキュメント | ✅ コマンド |

---

## 2. 理論的背景：なぜコンテキスト管理が重要か

### 2.1 開発ツールにおけるコンテキスト

開発ツールは毎回の会話で以下を読み込む：

```
┌─────────────────────────────────────────┐
│          コンテキストウィンドウ            │
│  ┌─────────────────────────────────┐   │
│  │ システム指示                      │   │
│  │ - ツール固有の設定                │   │
│  ├─────────────────────────────────┤   │
│  │ プロジェクトコンテキスト           │   │  ← ここを管理
│  │ - context.md / CLAUDE.md        │   │
│  │ - エージェント定義                │   │
│  ├─────────────────────────────────┤   │
│  │ 作業コンテキスト                  │   │
│  │ - 会話履歴                       │   │
│  │ - 開いているファイル              │   │
│  │ - ツール実行結果                  │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

**本システムが管理するのは「プロジェクトコンテキスト」の部分。**

### 2.2 コンテキスト肥大化の問題

トークン数が増えるほど、モデルの注意力は分散する（Context Rot）。

| 問題 | 説明 | 対策 |
|-----|------|------|
| **注意力の分散** | 情報が多すぎると重要な指示を見落とす | 必要最小限に絞る |
| **矛盾する情報** | 古い記述と新しい記述が衝突 | 定期的に整理・更新 |
| **無関係な情報** | タスクと関係ない情報がノイズになる | カテゴリ分離、参照パターン |

### 2.3 基本原則

**「最小限の高シグナル情報で、望む結果の確率を最大化する」**

| 方針 | 説明 | 実装 |
|-----|------|------|
| **圧縮** | 冗長を排除し、本質を残す | context.md を簡潔に保つ |
| **分離** | 詳細は別ファイルに切り出す | docs/ への参照パターン |
| **選択** | 必要な情報だけ読み込ませる | エージェント分割、ファイル分割 |

### 2.4 適切な抽象度（Right Altitude）

```
❌ 硬直的すぎる
   「変数名は必ずcamelCaseで、関数は20行以内で、
    インポートはアルファベット順で...」
   → ルールが多すぎて見落とされる、メンテナンスコスト高

❌ 曖昧すぎる
   「きれいなコードを書いてください」
   → 具体性がなく、効果が薄い

✅ 適切な抽象度
   「命名は意図を明確に。関数は単一責任を保つ。
    迷ったら可読性を優先」
   → 柔軟でありながら、明確な指針を提供
```

---

## 3. 目的・背景

### 3.1 解決したい課題

- 会話で得られた有用な指摘・ノウハウが散逸してしまう
- コンテキストファイルが肥大化し、効果が薄れる
- 繰り返し同じ指摘をする必要がある
- 専門的なワークフローのコンテキストが共有されにくい
- ツールを切り替えると蓄積した知識が活かせない

### 3.2 期待される効果

- 会話から学んだ内容を永続化して再利用
- 必要な情報だけを効率的に参照
- 肥大化したコンテキストを圧縮して最適化
- 複数ツール間でのコンテキスト共有

---

## 4. システム構成

### 4.1 ファイル構成

```
project-root/
├── .ai/                           # 汎用AIコンテキスト（SSOT）
│   ├── context.md                 # メインコンテキスト
│   ├── agents/                    # エージェント定義（対話・相談向け）
│   │   ├── _index.md              # エージェント一覧
│   │   └── architect.md           # 設計相談
│   ├── commands/                  # コマンド（アクション実行向け）
│   │   ├── context-update.md      # コンテキスト更新
│   │   ├── code-review.md         # コードレビュー実行
│   │   └── debug.md               # デバッグ支援
│   └── references/                # 参照用ファイル
│       ├── templates/             # ADR等のテンプレート
│       └── checklists/            # チェックリスト
│
├── docs/                          # 詳細ドキュメント（参照用）
│   ├── guidelines/                # コーディングガイドライン
│   ├── architecture/              # アーキテクチャ説明
│   └── decisions/                 # 設計判断の記録（ADR形式推奨）
│
├── .cursorrules                   # Cursor用（同期）
├── .cursor/rules/                 # Cursor用エージェント
├── .github/
│   └── copilot-instructions.md    # GitHub Copilot用
└── CLAUDE.md                      # Claude Code用
```

### 4.2 コンポーネントの役割

| コンポーネント | 役割 | 読み込みタイミング |
|---------------|------|------------------|
| `.ai/context.md` | メインコンテキスト。圧縮された重要情報 | **常時**（毎回読み込まれる） |
| `.ai/agents/` | エージェント定義（対話・相談向け） | **選択的**（呼び出し時） |
| `.ai/commands/` | コマンド定義（アクション実行向け） | **選択的**（実行時） |
| `.ai/references/` | テンプレート・チェックリスト | **必要時**（コマンドから参照） |
| `docs/` | 詳細ドキュメント | **必要時**（ツールが検索/参照） |

### 4.3 エージェント vs コマンドの使い分け

| 種類 | 用途 | 特徴 | 例 |
|-----|------|------|-----|
| エージェント | 対話・相談 | 継続的なやりとり | architect（設計相談） |
| コマンド | アクション実行 | ワンショット処理 | /code-review（レビュー実行） |

**判断基準**: エージェントとコマンドが1:1対応になる場合は、コマンドに統合してシンプルに保つ

### 4.4 参照パターン（Just-in-time）

context.md にはすべてを書かず、**詳細は docs/ への参照で対応**。

```markdown
<!-- context.md での記述例 -->

## アーキテクチャ
Clean Architecture採用。レイヤー間の依存は内向きのみ。
→ 詳細: docs/architecture/overview.md

## エラーハンドリング
Result型パターンを使用。例外は境界でのみキャッチ。
→ 詳細: docs/guidelines/error-handling.md
```

**メリット:**
- context.md を軽量に保てる
- ツールは必要に応じて docs/ を検索・参照
- 情報の重複を避けられる

### 4.5 エージェントファイル分割の指針

| 状況 | 推奨構成 |
|-----|---------|
| エージェント数 1〜2個 | 単一ファイル `.ai/agents.md` でOK |
| エージェント数 3個以上 | 個別ファイル `.ai/agents/*.md` に分割 |
| チーム開発 | 個別ファイル推奨（コンフリクト回避） |

**分割のメリット:**
- 必要なエージェントだけ参照可能（トークン節約）
- 個別に更新・バージョン管理しやすい

### 4.6 同期戦略

`.ai/` を正（Single Source of Truth）として、各ツール固有ファイルへ同期。

```
.ai/context.md (SSOT)
    ├── → .cursorrules
    ├── → .github/copilot-instructions.md
    └── → CLAUDE.md

.ai/agents/ (SSOT)
    ├── → .cursor/rules/
    └── → CLAUDE.md に追記
```

---

## 5. ワークフロー

### 5.1 コンテキスト保存フロー

```
┌─────────────────┐
│  AIとの会話     │
└────────┬────────┘
         ▼
┌─────────────────┐
│ 有用な指摘を識別 │
│ （手動で判断）   │
└────────┬────────┘
         ▼
┌─────────────────────────────────┐
│ 保存先を判断                     │
│ ・汎用ルール → context.md       │
│ ・専門ワークフロー → agents/     │
│ ・詳細情報 → docs/              │
└────────┬────────────────────────┘
         ▼
┌─────────────────┐
│ ツール別ファイル │
│ へ同期          │
└─────────────────┘
```

### 5.2 圧縮・整理フロー

context.md が肥大化したら圧縮。

| 指標 | 閾値 | アクション |
|-----|-----|----------|
| 行数 | 200行超 | 圧縮を検討 |
| 行数 | 300行超 | 要圧縮 |
| 重複記述 | 2箇所以上 | 統合 |
| 詳細すぎる記述 | - | docs/へ分離 |
| 古い情報 | 1ヶ月以上未更新 | 見直し・削除 |

**圧縮の手順:**
1. 重複の統合
2. 冗長な表現の簡潔化
3. 詳細情報を docs/ へ分離し、参照に置換
4. 古い情報の削除

---

## 6. 実行タイミング

### 6.1 トリガー一覧

| トリガー | 実行方法 | 推奨ユースケース |
|---------|---------|-----------------|
| 手動実行 | コマンド呼び出し | 重要な指摘を受けた直後 |
| セッション終了時 | 明示的に依頼 | 1日の作業終了時の振り返り |
| コミット時 | Git hook | コード変更と同期した更新 |
| 定期実行 | cron/GitHub Actions | 週次での圧縮・整理 |

### 6.2 Git Hook設定例

```bash
# .git/hooks/pre-commit
#!/bin/bash

if [ -f "scripts/sync-context.sh" ]; then
    bash scripts/sync-context.sh
    git add .cursorrules .github/copilot-instructions.md CLAUDE.md .cursor/rules/ 2>/dev/null || true
fi
```

---

## 7. コマンド定義

### 7.1 /context-update（コンテキスト更新）

会話からの学びを抽出し、整合性チェック・圧縮・保存を一括で実行。

**プロンプトテンプレート** (`.ai/commands/context-update.md`):

```markdown
# Context Update Command

このセッションを振り返り、コンテキストを更新してください。

## 実行手順

### Step 1: 抽出
この会話から保存すべき内容を特定：
- 新しく学んだこと
- 設計判断とその理由
- 踏んだ落とし穴・注意点

### Step 2: 整合性チェック
既存コンテキストとの確認：
- 矛盾する記述がないか
- 重複する内容がないか
- 古くなった情報がないか

### Step 3: 圧縮判断
context.md の現在の行数を確認：
- 200行以下 → そのまま追記
- 200行超 → 追記前に圧縮を実施

### Step 4: 保存先の判断

| 種類 | 保存先 |
|-----|-------|
| プロジェクト全般のルール | .ai/context.md |
| 設計判断とその理由 | docs/decisions/xxx.md |
| 詳細なガイドライン | docs/guidelines/xxx.md |
| 専門ワークフロー | .ai/agents/xxx.md |

## 圧縮方針（必要な場合）

1. **重複の統合**: 同じ内容を1つに
2. **参照化**: 詳細すぎる記述は docs/ へ分離し参照に置換
3. **削除**: 古くなった情報

## 出力形式

### 1. 変更サマリー
- 追加: [件数]
- 修正: [件数]
- 削除: [件数]
- 圧縮: [実施した/不要]

### 2. 更新内容

#### context.md
[変更後の全文、または差分]

#### その他のファイル（必要な場合）
- ファイルパス: [パス]
- 内容: [追記内容]

## 注意事項
- 適切な抽象度を保つ（硬直的すぎず、曖昧すぎず）
- 重要な情報は必ず保持（削除より分離を優先）
- 分離した情報は参照リンクを残す
```

---

## 8. エージェント定義

### 8.1 ファイル構成

```
.ai/agents/
├── _index.md              # エージェント一覧
├── code-reviewer.md       # コードレビュー専門
└── context-curator.md     # コンテキスト管理専門
```

### 8.2 インデックスファイル

`.ai/agents/_index.md`:

```markdown
# Project Agents

## エージェント一覧

| エージェント | ファイル | 役割 |
|-------------|---------|------|
| Code Reviewer | code-reviewer.md | コードレビューとベストプラクティス提案 |
| Context Curator | context-curator.md | コンテキストファイルの品質管理 |

## 共通ルール
- 各エージェントはプロジェクトの context.md に従う
- 不明点は推測せず確認を求める
```

### 8.3 個別エージェント定義例

`.ai/agents/code-reviewer.md`:

```markdown
# Code Reviewer

## 役割
コードレビューとベストプラクティスの提案

## 専門領域
- TypeScript/JavaScript
- Reactコンポーネント設計

## レビュー観点
- 型安全性
- コンポーネントの責務分離
- エラーハンドリング

## 参照すべきドキュメント
- docs/guidelines/coding-standards.md

## 出力形式
1. 重要度（🔴高/🟡中/🟢低）
2. 該当箇所
3. 問題点
4. 改善案
```

`.ai/agents/context-curator.md`:

```markdown
# Context Curator

## 役割
コンテキストファイルの品質管理と最適化

## 担当タスク
- context.md の定期的なレビューと圧縮
- 重複・矛盾の検出と解消
- docs/ 配下のドキュメント整理

## 使用コマンド
- /context-update

## 判断基準
- 200行を超えたら圧縮を検討
- 矛盾がないか常に確認
- 適切な抽象度を維持
```

### 8.4 エージェントの呼び出し方

```
「Code Reviewerとしてこのコードをレビューしてください」
「Context Curatorとしてコンテキストを整理してください」
```

---

## 9. 初期セットアップ

### 9.1 ディレクトリ作成

```bash
#!/bin/bash
# scripts/init-context.sh

mkdir -p .ai/agents .ai/commands
mkdir -p docs/guidelines docs/architecture docs/decisions

touch .ai/context.md
touch .ai/agents/_index.md

echo "✅ Context structure initialized!"
```

### 9.2 初期コンテキストのテンプレート

`.ai/context.md`:

```markdown
# Project Context

## プロジェクト概要
[1〜2文で簡潔に]

## 技術スタック
- 言語: 
- フレームワーク: 
- 主要ライブラリ: 

## コーディング方針
[適切な抽象度で記述]
→ 詳細: docs/guidelines/

## アーキテクチャ
[概要のみ]
→ 詳細: docs/architecture/

---
最終更新: YYYY-MM-DD
目標行数: 200行以内
```

### 9.3 同期スクリプト

`scripts/sync-context.sh`:

```bash
#!/bin/bash

SOURCE=".ai/context.md"
AGENTS_DIR=".ai/agents"

if [ ! -f "$SOURCE" ]; then
    echo "Error: $SOURCE not found"
    exit 1
fi

echo "=== Syncing context files ==="

# 行数チェック
LINE_COUNT=$(wc -l < "$SOURCE")
if [ "$LINE_COUNT" -gt 200 ]; then
    echo "⚠️  Warning: context.md is $LINE_COUNT lines (target: 200)"
fi

# Cursor用
cp "$SOURCE" .cursorrules 2>/dev/null && echo "✓ .cursorrules"

if [ -d "$AGENTS_DIR" ]; then
    mkdir -p .cursor/rules
    cp "$AGENTS_DIR"/*.md .cursor/rules/ 2>/dev/null && echo "✓ .cursor/rules/"
fi

# GitHub Copilot用
mkdir -p .github
cp "$SOURCE" .github/copilot-instructions.md && echo "✓ .github/copilot-instructions.md"

# Claude Code用
cp "$SOURCE" CLAUDE.md
if [ -d "$AGENTS_DIR" ]; then
    echo -e "\n---\n\n# Agents" >> CLAUDE.md
    for f in "$AGENTS_DIR"/*.md; do
        [ -f "$f" ] && cat "$f" >> CLAUDE.md && echo "" >> CLAUDE.md
    done
    echo "✓ CLAUDE.md (with agents)"
else
    echo "✓ CLAUDE.md"
fi

echo "=== Sync completed! ==="
```

---

## 10. ベストプラクティス

### 10.1 コンテキスト記述のガイドライン

| Do ✅ | Don't ❌ |
|------|---------|
| 適切な抽象度で記述 | 過度に詳細なルールを列挙 |
| 参照パターンを活用 | すべてを1ファイルに詰め込む |
| 定期的に圧縮・整理 | 肥大化を放置 |
| 矛盾がないか確認 | 古い情報を残したまま追記 |

### 10.2 圧縮のタイミング

```
context.md の状態
    │
    ├── 200行以下 → OK
    │
    ├── 200〜300行 → 圧縮を検討
    │
    └── 300行超 → 要圧縮
        └── /context-update を実行
```

### 10.3 設計判断の記録（ADR形式）

`docs/decisions/` には ADR（Architecture Decision Record）形式で記録すると便利。

```markdown
<!-- docs/decisions/001-state-management.md -->
# ADR-001: 状態管理ライブラリの選定

## ステータス
採用

## コンテキスト
Reactアプリの状態管理方法を決定する必要がある

## 決定
Zustandを採用

## 理由
- シンプルなAPI
- TypeScript親和性が高い
- バンドルサイズが小さい

## 却下した選択肢
- Redux: ボイラープレートが多い
- Jotai: 今回の規模には過剰
```

---

## 11. テンプレートリポジトリ構造

本システムを他プロジェクトで再利用・継続的に改善するための構造。

### 11.1 リポジトリ構成

```
ai-context-template/
├── README.md                    # 使い方・クイックスタート
├── CHANGELOG.md                 # テンプレートの変更履歴
├── LICENSE
│
├── template/                    # ← プロジェクトにコピーされる部分
│   ├── .ai/
│   │   ├── context.md           # 初期テンプレート（穴埋め形式）
│   │   ├── agents/
│   │   │   ├── _index.md
│   │   │   └── context-curator.md
│   │   └── commands/
│   │       └── context-update.md
│   ├── docs/
│   │   ├── guidelines/.gitkeep
│   │   ├── architecture/.gitkeep
│   │   └── decisions/.gitkeep
│   └── scripts/
│       ├── init-context.sh      # 初期化スクリプト
│       ├── sync-context.sh      # 同期スクリプト
│       └── setup-hooks.sh       # Git hooks セットアップ
│
├── docs/                        # テンプレート自体のドキュメント
│   ├── design.md                # 設計書（本ドキュメント）
│   └── customization.md         # カスタマイズガイド
│
└── examples/                    # 技術スタック別の記述例
    ├── typescript-react/
    │   └── .ai/context.md
    ├── python-fastapi/
    │   └── .ai/context.md
    └── go-api/
        └── .ai/context.md
```

### 11.2 ファイルの役割

| ファイル/ディレクトリ | 役割 |
|---------------------|------|
| `template/` | プロジェクトにコピーされる本体 |
| `docs/` | テンプレート自体の設計・使い方 |
| `examples/` | 技術スタック別のサンプル |
| `CHANGELOG.md` | バージョンごとの変更履歴 |
| `CLAUDE.md` | テンプレート開発用コンテキスト |

### 11.3 導入方法

```bash
# 初期化スクリプトを実行（既存プロジェクトに追加）
curl -sL https://raw.githubusercontent.com/your-org/ai-context-template/main/install.sh | bash
```

`install.sh` の内容：

```bash
#!/bin/bash
set -e

REPO="your-org/ai-context-template"
BRANCH="main"

echo "=== AI Context Template Installer ==="

# template/ 配下をダウンロード
curl -sL "https://github.com/$REPO/archive/refs/heads/$BRANCH.tar.gz" | tar xz --strip=2 "ai-context-template-$BRANCH/template"

# 実行権限を付与
chmod +x scripts/*.sh 2>/dev/null || true

# Git hooks をセットアップ（オプション）
read -p "Setup Git hooks? [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    bash scripts/setup-hooks.sh
fi

echo "✅ Done! Edit .ai/context.md to customize."
```

### 11.4 継続的改善のフロー

```
ai-context-template（テンプレートリポジトリ）
    │
    │  [リリース]
    ├── v1.0.0 ──→ プロジェクトA が採用
    │                  └── プロジェクト固有のカスタマイズ
    │
    │  [改善をマージ]
    ├── v1.1.0 ──→ プロジェクトB が採用
    │   └── commands/ の改善
    │
    │  [改善をマージ]
    ├── v1.2.0
    │   └── examples/ の追加
    │
    └── 各プロジェクトは CHANGELOG を見て必要に応じて手動で取り込み
```

### 11.5 改善の取り込み方

プロジェクトがテンプレートの更新を取り込む場合：

```bash
# 1. 変更点を確認
curl -s https://raw.githubusercontent.com/your-org/ai-context-template/main/CHANGELOG.md

# 2. 必要なファイルだけ取得
curl -sO https://raw.githubusercontent.com/your-org/ai-context-template/main/template/.ai/commands/context-update.md

# 3. または差分を確認して手動マージ
```

**注意**: プロジェクト固有のカスタマイズは `context.md` に集中するため、  
コマンドやスクリプトは比較的安全に更新できる。

### 11.6 バージョニング方針

| 変更内容 | バージョン | 例 |
|---------|-----------|-----|
| 破壊的変更（構造変更） | メジャー | v2.0.0 |
| 機能追加（新コマンド等） | マイナー | v1.1.0 |
| バグ修正・文言修正 | パッチ | v1.0.1 |

### 11.7 CHANGELOG.md のフォーマット

```markdown
# Changelog

## [1.1.0] - 2025-07-01

### Added
- examples/go-api/ を追加

### Changed
- context-update.md の圧縮判断ロジックを改善

### Fixed
- sync-context.sh の権限エラーを修正

## [1.0.0] - 2025-06-15

### Added
- 初回リリース
```

### 11.8 テンプレートリポジトリ用 CLAUDE.md

テンプレート自体を開発・改善するためのコンテキスト。

```markdown
# AI Context Template

## プロジェクト概要

AIコーディングアシスタント（Cursor、Claude Code、GitHub Copilot等）向けの
コンテキスト管理テンプレート。プロジェクトに導入して使う。

## リポジトリ構造

```
├── template/          # 配布される本体（ここを編集）
├── docs/              # 設計書・ガイド
├── examples/          # 技術スタック別サンプル
├── install.sh         # インストーラー
└── CHANGELOG.md       # 変更履歴（リリース時に更新必須）
```

## 開発方針

### コンテキスト設計の原則
- 最小限の高シグナル情報で効果を最大化
- 適切な抽象度を保つ（硬直的すぎず、曖昧すぎず）
- 詳細は参照パターンで対応（docs/へのリンク）

### ファイル編集時の注意

| ファイル | 注意点 |
|---------|--------|
| template/.ai/context.md | 穴埋め形式を維持。具体的すぎる例は避ける |
| template/.ai/commands/*.md | ツール非依存を維持 |
| template/scripts/*.sh | POSIX互換を維持（bash依存OK） |
| examples/**/context.md | 実際に使える具体例を記載 |

### 破壊的変更の定義
- template/ のディレクトリ構造変更
- コマンド名の変更
- 必須ファイルの追加・削除

## リリース手順

1. CHANGELOG.md を更新
2. バージョンタグを作成: `git tag v1.x.x`
3. プッシュ: `git push origin v1.x.x`

## よくある改善パターン

- 新しい技術スタックの examples/ 追加
- コマンドテンプレートの改善
- スクリプトのバグ修正・機能追加
- ドキュメントの明確化
```

---

## 12. 将来拡張

| 機能 | 説明 | 優先度 |
|-----|------|-------|
| 自動圧縮提案 | 閾値超過時に圧縮を提案 | 高 |
| 重複検出 | 類似コンテキストの自動検出 | 中 |
| チーム共有 | 複数開発者間でのコンテキスト共有 | 中 |
| 変更履歴 | コンテキスト変更の差分管理 | 低 |

---

## 13. 参考資料

### コンテキスト管理の理論
- [Effective context engineering for AI agents - Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Context Engineering - LangChain Blog](https://blog.langchain.com/context-engineering-for-agents/)

### ツール別ドキュメント
- [Cursor Rules](https://docs.cursor.com)
- [GitHub Copilot Instructions](https://docs.github.com/en/copilot)
- [Claude Code](https://docs.anthropic.com)

---

*Document Version: 2.0.0*  
*Last Updated: 2025-06*
