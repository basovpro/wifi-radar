"""
Alembic environment for WiFi-Radar.

▪ Работаем только со схемой `public`.
▪ Любые объекты, отсутствующие в Base.metadata, игнорируются при
  автогенерации, поэтому Alembic не трогает системные таблицы PostGIS.
"""

from logging.config import fileConfig
import os
import sys

from alembic import context
from sqlalchemy import engine_from_config, pool  # type: ignore
from dotenv import load_dotenv

# ── 1. Добавляем backend/app в PYTHONPATH ─────────────────────────
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Импортируем Base и ВСЕ модели, чтобы они зарегистрировались в metadata
from app.db import Base  # type: ignore  # noqa: E402
import app.models  # noqa: E402,F401  (сам факт импорта достаточно)

# ── 2. Загрузка переменных окружения ─────────────────────────────
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

# Используем отдельные переменные для каждого компонента БД
DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "radar")
DB_USER = os.getenv("DB_USER", "radar")
DB_PASS = os.getenv("DB_PASS", "radar")

# Собираем URL из компонентов
DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ── 3. Конфигурация и логирование ─────────────────────────────────
config = context.config
fileConfig(config.config_file_name)

# Переопределяем sqlalchemy.url из переменных окружения
config.set_main_option("sqlalchemy.url", DATABASE_URL)

target_metadata = Base.metadata  # ← набор таблиц из моделей


# ── 4. Фильтр объектов ────────────────────────────────────────────
def include_object(obj, name, type_, reflected, compare_to):
    """
    • Если объект отражён из БД (`reflected`) и отсутствует в Base.metadata
      (`compare_to is None`) — игнорируем (False).
    • Иначе — учитываем (True).

    Таким образом Alembic видит ТОЛЬКО наши модели и ничего не удаляет
    из расширений postgis_tiger_geocoder / postgis_topology.
    """
    return not (reflected and compare_to is None)


# ── 5. Запуск миграций (online-mode) ──────────────────────────────
def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,
            include_schemas=True,  # нужен, чтобы Alembic видел schema объекта
        )

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
