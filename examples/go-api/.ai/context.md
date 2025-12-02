# Project Context

## プロジェクト概要
Go言語を使用したREST APIサーバー

## 技術スタック
- 言語: Go 1.22
- ルーター: chi
- ORM: sqlc
- バリデーション: go-playground/validator
- テスト: testing, testify

## コーディング方針
- エラーは必ずハンドリング
- インターフェースは使う側で定義
- ゴルーチンはcontext.Contextで制御
- 命名はシンプルに、略語は慎重に

→ 詳細: docs/guidelines/

## アーキテクチャ
標準的なレイヤードアーキテクチャ

```
.
├── cmd/
│   └── api/         # エントリポイント
├── internal/
│   ├── handler/     # HTTPハンドラ
│   ├── service/     # ビジネスロジック
│   ├── repository/  # データアクセス
│   └── model/       # ドメインモデル
├── pkg/             # 公開パッケージ
└── sql/
    └── queries/     # sqlcクエリ
```

→ 詳細: docs/architecture/

## エラーハンドリング
- カスタムエラー型を定義
- エラーはラップして伝播
- ログはslog（構造化ログ）

→ 詳細: docs/guidelines/error-handling.md

## テスト方針
- テーブル駆動テスト
- testcontainersでDB統合テスト
- モックは最小限に

---
最終更新: 2025-01
目標行数: 200行以内
