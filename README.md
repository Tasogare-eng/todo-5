# TODO リスト Web アプリ (MVP)

シンプルなタスク管理 CRUD。FastAPI + SQLite (API) / Vue 3 + Vite + Tailwind (フロント)。

## 特徴
- 1日開発想定の最小構成
- 将来認証やタグ機能へ拡張しやすい設計
- OSS (MIT License)

## 技術スタック
| レイヤ | 技術 |
|--------|------|
| フロント | Vue 3, TypeScript, Vite, Tailwind CSS |
| バックエンド | FastAPI, SQLModel, Alembic |
| DB | SQLite |
| テスト | pytest (API), Playwright (E2E) |

## ディレクトリ構成（抜粋）
```
backend/
  app/
    main.py
    api/
    models/
    schemas/
    db/
frontend/
  src/
    components/
    api/
```

## セットアップ
### 共通
```
git clone <repo>
cd <repo>
```

### Backend 開発起動
```
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
データベース: `sqlite:///./data/app.db` (初回テーブルは Alembic マイグレーションで生成予定)。

### Frontend 開発起動
```
cd frontend
npm install
npm run dev
```
フロントURL: http://localhost:5173  (環境変数: `.env.development` で `VITE_API_BASE_URL` 指定)

## テスト
### Backend (pytest + coverage)
```
pytest backend/tests -q --cov=backend/app --cov-report=term-missing
```

### E2E (Playwright)
```
# 端末1
uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port 8000
# 端末2
cd frontend
npm run test:e2e
```

## CI
GitHub Actions: `.github/workflows/ci.yml`
- backend: lint (ruff), pytest + coverage
- frontend: lint, Playwright (Chromium/Firefox/WebKit)

## コミット規約 (簡易)
`<type>: <subject>` 形式を推奨
- feat: 機能追加
- fix: バグ修正
- docs: ドキュメント
- chore: 雑務/依存
- refactor: リファクタ
- test: テスト追加/修正

## ブランチ戦略
- main: 安定 / リリース
- feature/*: 機能開発
PR 経由で main へマージ。必須: テストパス。

## デプロイ (予定 → 実施手順)
### Backend (Railway)
1. Railway で New Project → GitHub リポジトリ接続
2. Root or backend ディレクトリを選択 (この構成では repo 直下で Dockerfile は `backend/` 配下なので Railway の設定で `backend` を指定する)
3. 環境変数設定（例）:
   - `ENVIRONMENT=production`
   - `CORS_ORIGINS=https://<your-vercel-domain>` (複数ならカンマ区切り)
   - `DATABASE_URL` (Railway の Postgres を使うなら接続文字列をそのまま設定。SQLite のままでも動作可)
   - `GIT_SHA` (任意: GitHub Actions から注入する場合)
4. デプロイ後ヘルス確認: `GET /health` (version/git_sha/env)
5. 本番 CORS 設定が正しいかフロントから fetch で確認

### Frontend (Vercel)
1. New Project → GitHub リポジトリ選択
2. Framework Preset: Vite (Auto)
3. 環境変数設定:
   - `VITE_API_BASE_URL=https://<railway-app-domain>`
4. デプロイ後ブラウザで CRUD 動作確認

### 共通ヘルスエンドポイント
- Liveness: `/healthz` → `{ "ok": true }`
- Readiness: `/health` → env, version, git_sha を返却

### バージョンタグ
```
git tag v0.1.0
git push origin v0.1.0
```

## API 概要
- GET /api/tasks
- POST /api/tasks
- GET /api/tasks/{id}
- PUT /api/tasks/{id}
- PATCH /api/tasks/{id}
- DELETE /api/tasks/{id}

## ライセンス
MIT
