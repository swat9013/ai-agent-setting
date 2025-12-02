# Customization Guide

このガイドでは、テンプレートをプロジェクトに合わせてカスタマイズする方法を説明します。

## 基本的なカスタマイズ

### context.md の編集

`.ai/context.md` はプロジェクトのメインコンテキストファイルです。

```markdown
# Project Context

## プロジェクト概要
ユーザー認証機能を持つWebアプリケーション

## 技術スタック
- 言語: TypeScript
- フレームワーク: Next.js 14
- 主要ライブラリ: Prisma, NextAuth.js

## コーディング方針
- Server Componentsをデフォルトで使用
- データフェッチはServer Actionsで実装
- 型安全性を最優先
```

### 適切な抽象度

| 避けるべき | 推奨 |
|-----------|------|
| 変数名は必ずcamelCaseで... | 命名は意図を明確に |
| 関数は20行以内で... | 関数は単一責任を保つ |
| きれいなコードを書いて | 可読性を優先、複雑さは最小限に |

## エージェントの追加

### 新しいエージェントを作成

1. `.ai/agents/` に新しいファイルを作成
2. `_index.md` に追加

例: `.ai/agents/code-reviewer.md`

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

## 出力形式
1. 重要度（高/中/低）
2. 該当箇所
3. 問題点
4. 改善案
```

## ドキュメントの構造

### docs/guidelines/

コーディングガイドラインを配置します。

```
docs/guidelines/
├── coding-standards.md
├── error-handling.md
└── testing.md
```

### docs/architecture/

アーキテクチャドキュメントを配置します。

```
docs/architecture/
├── overview.md
├── data-flow.md
└── folder-structure.md
```

### docs/decisions/

ADR（Architecture Decision Record）形式で設計判断を記録します。

```markdown
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
```

## コマンドの追加

`.ai/commands/` にコマンドテンプレートを追加できます。

例: `.ai/commands/review.md`

```markdown
# Review Command

以下の観点でコードをレビューしてください：

1. 型安全性
2. エラーハンドリング
3. パフォーマンス
4. セキュリティ

出力形式：
- 問題点と改善案をリストで提示
- 重要度を明記
```

## 同期のカスタマイズ

### 特定ツールへの同期を無効化

`scripts/sync-context.sh` を編集して、不要な同期をコメントアウトします。

```bash
# Cursor（無効化する場合はコメントアウト）
# cp "$SOURCE" .cursorrules

# GitHub Copilot
mkdir -p .github
cp "$SOURCE" .github/copilot-instructions.md
```

### 同期内容のカスタマイズ

ツール固有の内容を追加する場合は、同期スクリプトを編集します。

```bash
# Claude Code用に追記
cp "$SOURCE" CLAUDE.md
echo -e "\n## Claude Code固有の設定\n..." >> CLAUDE.md
```

## ベストプラクティス

1. **context.md は200行以内に保つ**
2. **詳細は docs/ に分離し、参照パターンを使う**
3. **定期的に /context-update を実行して整理する**
4. **エージェントは必要に応じて追加する**
