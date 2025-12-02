# ai-coding-setting

AIコーディングアシスタント（Cursor、Claude Code、GitHub Copilot等）向けのコンテキスト管理テンプレート。

## 概要

会話から得られた指摘やノウハウを体系的に保存し、プロジェクトの成長とともにコンテキストも進化させるための仕組みを提供します。

### 対応ツール

| ツール | コンテキストファイル | 同期対象 |
|--------|---------------------|----------|
| Cursor | `.cursorrules`, `.cursor/rules/` | ✅ |
| GitHub Copilot | `.github/copilot-instructions.md` | ✅ |
| Claude Code | `CLAUDE.md` | ✅ |
| Codex CLI | `AGENTS.md` | ✅ |

## クイックスタート

### インストール

```bash
curl -sL https://raw.githubusercontent.com/your-org/ai-coding-setting/main/install.sh | bash
```

または手動でコピー:

```bash
git clone https://github.com/your-org/ai-coding-setting.git
cp -r ai-coding-setting/template/* your-project/
```

### セットアップ

```bash
# 1. context.md を編集
vi .ai/context.md

# 2. ツール固有ファイルへ同期
bash scripts/sync-context.sh

# 3. (オプション) Git hooks を設定
bash scripts/setup-hooks.sh
```

## ディレクトリ構造

```
your-project/
├── .ai/                      # AIコンテキスト（SSOT）
│   ├── context.md            # メインコンテキスト
│   ├── agents/               # エージェント定義
│   │   ├── _index.md
│   │   └── context-curator.md
│   └── commands/             # コマンドテンプレート
│       └── context-update.md
├── docs/                     # 詳細ドキュメント
│   ├── guidelines/
│   ├── architecture/
│   └── decisions/
├── scripts/                  # ユーティリティスクリプト
│   ├── sync-context.sh
│   └── setup-hooks.sh
├── .cursorrules              # Cursor用（自動生成）
├── .github/
│   └── copilot-instructions.md  # Copilot用（自動生成）
└── CLAUDE.md                 # Claude Code用（自動生成）
```

## 使い方

### コンテキストの更新

会話から有用な情報を得たら、`/context-update` コマンド（または `.ai/commands/context-update.md` のプロンプト）を使用してコンテキストを更新します。

### 同期

`.ai/context.md` を編集した後、同期スクリプトを実行:

```bash
bash scripts/sync-context.sh
```

Git hooks を設定している場合は、コミット時に自動同期されます。

### 圧縮

context.md が200行を超えたら圧縮を検討してください:

1. 重複の統合
2. 詳細を docs/ に分離
3. 古い情報の削除

## ベストプラクティス

- **context.md は200行以内に保つ**
- **詳細は docs/ に分離し、参照パターンを使う**
- **適切な抽象度を保つ**（硬直的すぎず、曖昧すぎず）
- **定期的に整理・圧縮する**

## 技術スタック別サンプル

- [TypeScript + React](./examples/typescript-react/)
- [Python + FastAPI](./examples/python-fastapi/)
- [Go API](./examples/go-api/)

## ドキュメント

- [設計書](./docs/design.md)
- [カスタマイズガイド](./docs/customization.md)
