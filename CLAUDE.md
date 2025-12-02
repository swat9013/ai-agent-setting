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
