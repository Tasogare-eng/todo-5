# 08 デプロイ & 運用

## 概要
Vercel (フロント) / Railway (API) デプロイ手順と運用タスク。

## タスクリスト
- [ ] Railway プロジェクト作成
- [ ] Railway 環境変数設定 (PYTHONUNBUFFERED=1 など)
- [ ] Dockerfile ビルド確認（本番用: --no-cache）
- [ ] マイグレーション自動実行エントリ (起動時 Alembic upgrade)
- [ ] Vercel プロジェクト作成
- [ ] フロント環境変数 (VITE_API_BASE_URL) 設定
- [ ] CORS 本番 Origin 設定
- [ ] デプロイ後動作確認 (CRUD) 
- [ ] バージョンタグ付け (v0.1.0)
- [ ] README にデモURL追記

## 完了条件
- 公開 URL で CRUD 動作
- schema 最新マイグレーション適用済

## メモ
スキーマ変更時は手動で `alembic revision --autogenerate` → デプロイ時 upgrade。
