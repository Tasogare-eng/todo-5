# 02 バックエンド基盤（FastAPI + SQLModel）

## 概要
FastAPI プロジェクト雛形・依存追加・アプリ起動確認まで。

## タスクリスト
- [x] pyproject.toml or requirements.txt 作成（fastapi, uvicorn, sqlmodel, alembic, pydantic-settings, ruff, pytest 等）
- [x] 仮想環境 or poetry/pipenv 選定（簡易: venv）
- [x] `app/main.py` エントリ作成 (健康チェック `/health`)
- [x] 設定モジュール（環境変数読み込み）
- [x] ロガー設定（構造化: path, status, duration）
- [x] CORS 設定（フロント想定 Origin 許可）
- [x] Dockerfile 作成
- [x] docker-compose.yml（dev 用, volumes: SQLite）
- [x] Alembic 初期化 & env.py SQLModel 対応
- [x] Ruff 設定ファイル（pyproject.toml）
- [x] VSCode 拡張向け設定（.vscode/settings.json 任意）

## 完了条件
- `uvicorn app.main:app` がローカルで起動し /health が 200
- Docker ビルド・起動成功

## メモ
Railway デプロイ時は Dockerfile 利用。Python 3.12 ベース想定。
