from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time
from app.core.config import get_settings
from app.core.logging.logger import log_requests
from app.api.routes.tasks import router as tasks_router
from urllib.parse import urlparse

settings = get_settings()
app = FastAPI(title="Todo API", version="0.1.0")

@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = (time.time() - start_time) * 1000
    response.headers["X-Process-Time-ms"] = f"{duration:.2f}"
    return response

@app.on_event("startup")
async def startup_event():
    # Alembic はコンテナ CMD で実行済み想定
    print("[startup] application initialized")

app.include_router(tasks_router)

app.middleware("http")(log_requests)

# 本番デプロイ時は cors_origins に Railway / Vercel の正規URLをカンマ区切りで設定
origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "env": settings.environment,
        "version": app.version,
        "git_sha": settings.git_sha,
    }

@app.get("/healthz")
async def healthz():
    # readiness 用（将来 DB 接続チェックなど拡張可）
    return {"ok": True}
