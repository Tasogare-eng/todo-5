# 03 Task モデル & CRUD API 実装

## 概要
Task エンティティ定義・DBマイグレーション・CRUD エンドポイント実装。

## タスクリスト
- [x] Task SQLModel 定義（id UUID, title, description, status enum, priority enum, dueDate, createdAt, updatedAt）
- [x] Enum 定義 (Status: todo/doing/done, Priority: high/medium/low)
- [x] Pydantic スキーマ（Create / Update / Read）
- [x] Alembic マイグレーション生成 & 適用
- [x] DB セッション依存性 (sessionmaker) 実装
- [x] CRUD リポジトリ関数（list/filter, get, create, update, delete）
- [x] ルータ `/api/tasks` 実装
- [x] バリデーション（タイトル長等）確認テスト
- [x] エラーハンドラ（404, 400）
- [x] 自動並び順 createdAt DESC 適用

## 完了条件
- 全 CRUD エンドポイントが仕様通りレスポンス
- マイグレーションでテーブル生成
- ステータスフィルタ実装 `/api/tasks?status=todo`

## メモ
PATCH 対応は余裕時。必須でなければ PUT のみ先行。
