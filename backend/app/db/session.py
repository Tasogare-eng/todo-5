from __future__ import annotations
from sqlmodel import create_engine, Session
from app.core.config import get_settings
from typing import Generator

settings = get_settings()
DATABASE_URL = settings.database_url
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args)

# FastAPI の Depends で利用する generator 関数
# 注意: contextmanager デコレータは付与しない

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
