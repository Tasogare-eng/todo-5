# 09 将来拡張・リファクタリング計画

## 概要
MVP 後の改善・拡張アイテム管理。

## タスクリスト
- [ ] 認証導入（OAuth / JWT）設計検討
- [ ] user テーブル追加 & Task へ user_id 外部キー
- [ ] タグ機能 (tags / task_tags 中間)
- [ ] 検索最適化 (インデックス / FTS5)
- [ ] 論理削除 (deletedAt) 導入とクエリフィルタ共通化
- [ ] サービス層抽出 (repository / service / router 分離)
- [ ] エラーハンドリング共通化ミドルウェア
- [ ] CI 強化 (lint/test/e2e 並列)
- [ ] パフォーマンス計測 (profiling)
- [ ] PWA 化
- [ ] 国際化 (i18n plugin)
- [ ] ダークモード切替
- [ ] 通知ジョブ (Celery / APScheduler)

## 完了条件
- 優先度付け & 次リリース計画決定

## メモ
Backlog 的に扱い、Issue 化していく。
