# Project Context

## プロジェクト概要
TypeScript + Reactを使用したWebアプリケーション

## 技術スタック
- 言語: TypeScript 5.x
- フレームワーク: React 18 / Next.js 14
- 状態管理: Zustand
- スタイリング: Tailwind CSS
- テスト: Vitest, React Testing Library

## コーディング方針
- 型安全性を最優先。any は使わない
- Server Componentsをデフォルトで使用
- コンポーネントは単一責任を保つ
- カスタムフックでロジックを分離

→ 詳細: docs/guidelines/

## アーキテクチャ
Feature-based構造を採用

```
src/
├── app/           # Next.js App Router
├── components/    # 共有UIコンポーネント
├── features/      # 機能ごとのモジュール
│   └── [feature]/
│       ├── components/
│       ├── hooks/
│       └── types/
├── lib/           # ユーティリティ
└── types/         # グローバル型定義
```

→ 詳細: docs/architecture/

## エラーハンドリング
- Result型パターンを使用
- 例外はAPI境界でのみキャッチ
- ユーザー向けエラーメッセージは i18n 対応

→ 詳細: docs/guidelines/error-handling.md

## テスト方針
- ユニットテスト: ビジネスロジックを重点的に
- 統合テスト: ユーザーフローを検証
- カバレッジ目標: 80%以上

---
最終更新: 2025-01
目標行数: 200行以内
