import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.db import Base, engine, SessionLocal
from app import models


# ── создаём/чистим таблицы один раз за сессию ──────────────────
@pytest.fixture(scope="session", autouse=True)
def _prepare_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# ── очищаем данные перед каждым тестом ─────────────────────────
@pytest.fixture(autouse=True)
def _clean_db():
    """Очищаем все данные перед каждым тестом."""
    session = SessionLocal()
    try:
        # Удаляем все записи из всех таблиц
        session.query(models.Ping).delete()
        session.query(models.Hotspot).delete()
        session.commit()
    finally:
        session.close()


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
