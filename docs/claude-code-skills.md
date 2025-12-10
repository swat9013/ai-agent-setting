# Claude Code Skills ガイド

Claude Code の Agent Skills 機能についてのリファレンス。

## 概要

**Agent Skills** は専門知識を再利用可能な機能にパッケージ化したもの。
`SKILL.md` ファイルとサポートファイルで構成される。

### 主な特徴

| 特徴 | 説明 |
|-----|------|
| モデル駆動型 | ユーザーが明示的に呼び出す必要なし。Claudeが自動判断 |
| チーム共有 | Git経由でプロジェクト全体に配布可能 |
| 複合構成 | スクリプト、テンプレート等の複数ファイルで構成可 |
| 段階的開示 | 必要時のみ関連ファイルを読み込み |

## ファイル構造

```
.claude/skills/my-skill-name/
├── SKILL.md                 # 必須
├── reference.md             # オプション
├── scripts/
│   └── helper.py           # オプション
└── templates/
    └── template.txt        # オプション
```

### 配置場所（スコープ）

| スコープ | パス | 用途 |
|---------|------|------|
| Personal | `~/.claude/skills/` | 個人ワークフロー、実験 |
| Project | `.claude/skills/` | チーム共有（Git管理） |
| Plugin | Plugin内 `skills/` | マーケットプレイス配布 |

## SKILL.md の書き方

### 基本構造

```yaml
---
name: your-skill-name
description: Brief description of what this Skill does and when to use it
allowed-tools: Read, Grep, Glob  # オプション
---

# Your Skill Name

## Instructions
具体的な手順を記載

## Examples
使用例を記載
```

### Frontmatter フィールド

| フィールド | 説明 | 制限 |
|-----------|------|------|
| `name` | 一意な識別子 | 小文字・数字・ハイフンのみ、最大64文字 |
| `description` | 何をするか、いつ使うか | 最大1024文字。**発見に最重要** |
| `allowed-tools` | 使用ツール制限 | オプション。指定時はそのツールのみ使用可 |

## Slash Commands との比較

| 観点 | Slash Commands | Agent Skills |
|-----|---------------|--------------|
| 複雑さ | シンプル | 複雑な機能向け |
| 構成 | 単一 `.md` | ディレクトリ（複数ファイル可） |
| 呼び出し | 明示的（`/command`） | 自動発見 |
| 用途 | 繰り返すプロンプト | 複合ワークフロー |

### 使い分けの指針

**Slash Commands**: 同じプロンプトを繰り返す、実行タイミングを制御したい

**Agent Skills**: 自動発見させたい、複数ファイル・スクリプトが必要、チーム標準化

## ベストプラクティス

### 1. Description を具体的に書く（最重要）

Claudeの発見能力を最大化するため、Description は具体的に記述する。

```yaml
# Good - 発見されやすい
description: Extract text and tables from PDF files, fill forms, merge documents.
Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.

# Bad - 曖昧で発見されない
description: Helps with documents
```

**含めるべき要素**:
- 何ができるか（機能）
- いつ使うか（トリガーキーワード）
- サポートするファイル形式

### 2. 1 Skill = 1 機能（集中度を保つ）

```yaml
# Good - 集中した設計
- PDF form filling
- Excel data analysis
- Git commit messages

# Bad - 責任が大きすぎる（分割すべき）
- Document processing
- Data tools
```

### 3. allowed-tools でセキュリティ制御

読み取り専用やスコープ限定のワークフローに有効。

```yaml
---
name: safe-file-reader
description: Read files without making changes.
allowed-tools: Read, Grep, Glob
---
```

### 4. チームテストで発見性を検証

- 期待したタイミングで発動するか
- 説明文は明確か
- エッジケースの対応

### 5. その他

- ファイルパスは Unix 形式で統一（`scripts/helper.py`）
- 依存パッケージは Description に明記
- バージョン履歴をドキュメント化

## 実装例

### シンプルな Skill（単一ファイル）

```yaml
---
name: generating-commit-messages
description: Generates clear commit messages from git diffs.
Use when writing commit messages or reviewing staged changes.
---

# Generating Commit Messages

## Instructions

1. Run `git diff --staged` to see changes
2. Summary under 50 characters
3. Use present tense
4. Explain what and why, not how
```

### 読み取り専用 Skill

```yaml
---
name: code-reviewer
description: Review code for best practices and potential issues.
Use when reviewing code, checking PRs, or analyzing code quality.
allowed-tools: Read, Grep, Glob
---

# Code Reviewer

## Review checklist

1. Code organization and structure
2. Error handling
3. Performance considerations
4. Security concerns
```

### 複数ファイル構成

```
pdf-processing/
├── SKILL.md
├── FORMS.md
├── REFERENCE.md
└── scripts/
    ├── fill_form.py
    └── validate.py
```

**SKILL.md**:
```yaml
---
name: pdf-processing
description: Extract text, fill forms, merge PDFs.
Use when working with PDF files, forms, or document extraction.
Requires pypdf and pdfplumber packages.
---

# PDF Processing

## Quick start

For form filling, see [FORMS.md](FORMS.md).
For detailed API reference, see [REFERENCE.md](REFERENCE.md).

## Requirements

pip install pypdf pdfplumber
```

## トラブルシューティング

### Skill が発動しない

| 原因 | 対処 |
|-----|------|
| Description が不十分 | 具体的なキーワードを追加 |
| YAML パースエラー | タブ→スペース、`---` の確認 |
| ファイルパス不正 | `ls .claude/skills/` で確認 |
| 複数 Skill の競合 | Description をより具体的に区別 |

### デバッグ方法

```bash
# デバッグモードで起動
claude --debug

# Skills 一覧確認
ls ~/.claude/skills/
ls .claude/skills/

# 特定 Skill の内容確認
cat .claude/skills/my-skill/SKILL.md
```

### 注意点

- 変更反映には Claude Code の再起動が必要
- スクリプトは `chmod +x` で実行権限を付与
- `allowed-tools` は Claude Code のみ対応

## 参考

- [Skills Documentation](https://code.claude.com/docs/en/skills.md)
- [Slash Commands](https://code.claude.com/docs/en/slash-commands.md)
- [Plugins](https://code.claude.com/docs/en/plugins.md)
