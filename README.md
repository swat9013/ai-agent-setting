# ai-agent-setting

AIコーディングアシスタント（Cursor、Claude Code、GitHub Copilot等）向けのコンテキスト管理テンプレート。

## 概要

会話から得られた指摘やノウハウを体系的に保存し、プロジェクトの成長とともにコンテキストも進化させるための仕組みを提供します。

### 対応ツール

| ツール         | コンテキストファイル                 | 同期対象 |
| -------------- | ------------------------------------ | -------- |
| Cursor         | `.cursorrules`, `.cursor/rules/` | ✅       |
| GitHub Copilot | `.github/copilot-instructions.md`  | ✅       |
| Claude Code    | `CLAUDE.md`                        | ✅       |

## クイックスタート

### インストール

```bash
curl -sL https://raw.githubusercontent.com/swat9013/ai-agent-setting/main/install.sh | bash
```

または手動でコピー:

```bash
git clone https://github.com/swat9013/ai-agent-setting.git
cp -r ai-agent-setting/template/.ai your-project/
cp -r ai-agent-setting/template/docs your-project/
```

### セットアップ

```bash
# 1. context.md を編集
vi .ai/context.md

# 2. ツール固有ファイルへ同期
python3 .ai/scripts/sync-context.py

# 3. (オプション) Git hooks を設定
bash .ai/scripts/setup-hooks.sh
```

## リポジトリ構造

```
ai-agent-setting/
├── template/              # 配布される本体
│   ├── .ai/
│   │   ├── context.md     # メインコンテキスト（穴埋め形式）
│   │   ├── agents/        # エージェント定義
│   │   ├── commands/      # コマンドテンプレート
│   │   ├── references/    # チェックリスト・テンプレート等
│   │   └── scripts/       # ユーティリティスクリプト
│   └── docs/              # プロジェクト用ドキュメント雛形
├── docs/                  # 本テンプレートの設計書・ガイド
├── examples/              # 技術スタック別サンプル
├── install.sh             # インストーラー
└── CHANGELOG.md           # 変更履歴
```

### 導入後のプロジェクト構造

```
your-project/
├── .ai/                      # AIコンテキスト（SSOT）
│   ├── context.md            # メインコンテキスト
│   ├── agents/               # エージェント定義
│   │   └── architect.md      # 設計相談エージェント
│   ├── commands/             # コマンドテンプレート
│   │   ├── code-review.md
│   │   ├── context-update.md
│   │   ├── critical-think.md
│   │   └── debug.md
│   ├── references/           # 参照用ファイル
│   │   ├── checklists/
│   │   └── templates/
│   └── scripts/              # ユーティリティ
│       ├── measure-context.py
│       ├── sync-context.py
│       └── setup-hooks.sh
├── docs/                     # 詳細ドキュメント
├── .cursorrules              # Cursor用（自動生成）
├── .github/
│   └── copilot-instructions.md  # Copilot用（自動生成）
└── CLAUDE.md                 # Claude Code用（自動生成）
```

## 使い方

### コンテキストの更新

会話から有用な情報を得たら、`/context-update` コマンドを使用してコンテキストを更新します。

### 同期

`.ai/context.md` を編集した後、同期スクリプトを実行:

```bash
python3 .ai/scripts/sync-context.py
```

Git hooks を設定している場合は、コミット時に自動同期されます。

### コンテキストの計測

コンテキストの規模を計測し、閾値超過をチェック:

```bash
python3 .ai/scripts/measure-context.py
python3 .ai/scripts/measure-context.py --context  # context.md のみ
```

## ベストプラクティス

- **context.md は簡潔に保つ**（推奨 1,500トークン以内）
- **詳細は docs/ に分離し、必要に応じて参照する**
- **適切な抽象度を保つ**（硬直的すぎず、曖昧すぎず）
- **定期的に整理・圧縮する**

## 技術スタック別サンプル

- [TypeScript + React](./examples/typescript-react/)
- [Python + FastAPI](./examples/python-fastapi/)
- [Go API](./examples/go-api/)

## ドキュメント

- [設計書](./docs/design.md)
- [カスタマイズガイド](./docs/customization.md)
