import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.db import Base, engine, SessionLocal


# ── создаём/чистим таблицы один раз за сессию ──────────────────
@pytest.fixture(scope="session", autouse=True)
def _prepare_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# ── фикстура «сырое соединение к БД» ───────────────────────────
@pytest.fixture
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


# ── фикстура «HTTP-клиент» ─────────────────────────────────────
@pytest.fixture
def client():
    return TestClient(app)
