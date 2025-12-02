# Project Context

## プロジェクト概要
Python + FastAPIを使用したREST APIサーバー

## 技術スタック
- 言語: Python 3.12
- フレームワーク: FastAPI
- ORM: SQLAlchemy 2.0
- バリデーション: Pydantic v2
- テスト: pytest, pytest-asyncio

## コーディング方針
- 型ヒントを必ず付ける
- async/awaitを積極的に使用
- 依存性注入パターンを活用
- docstringはGoogle形式

→ 詳細: docs/guidelines/

## アーキテクチャ
Clean Architecture採用。レイヤー間の依存は内向きのみ。

```
src/
├── api/           # エンドポイント定義
│   └── v1/
├── core/          # 設定、セキュリティ
├── domain/        # ビジネスロジック
│   ├── models/
│   └── services/
├── infrastructure/  # DB、外部サービス
│   └── repositories/
└── schemas/       # Pydanticスキーマ
```

→ 詳細: docs/architecture/

## エラーハンドリング
- カスタム例外クラスを使用
- HTTPExceptionでラップしてレスポンス
- ログは構造化ログ（JSON形式）

→ 詳細: docs/guidelines/error-handling.md

## テスト方針
- pytest-asyncioで非同期テスト
- Factoryパターンでテストデータ生成
- テスト用DBはSQLiteを使用

---
最終更新: 2025-01
目標行数: 200行以内
