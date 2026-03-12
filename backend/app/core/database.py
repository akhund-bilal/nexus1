from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings


def _connect_args() -> dict:
    if settings.postgres_dsn.startswith("sqlite"):
        return {"check_same_thread": False}
    return {}


engine = create_engine(settings.postgres_dsn, pool_pre_ping=True, connect_args=_connect_args())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
