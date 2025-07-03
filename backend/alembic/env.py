"""
Alembic environment for WiFi-Radar
Создан для работы только со схемой `public`; любые объекты,
которых нет в Base.metadata, игнорируются при автогенерации.
"""

from logging.config import fileConfig
import os
import sys

from alembic import context
from sqlalchemy import engine_from_config, pool

# ── 1. Добавляем каталог backend/app в PYTHONPATH ─────────────────
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app"))
)
from db import Base  # noqa: E402  (импорт после изменения sys.path)

# ── 2. Конфигурация и логирование ─────────────────────────────────
config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata  # наши модели

# ── 3. Функция-фильтр: включаем ТОЛЬКО объекты, описанные в моделях ─
def include_object(obj, name, type_, reflected, compare_to):
    """
    • compare_to is None  ⇒ объекта нет в models  ⇒ игнорируем (False)
    • иначе               ⇒ это наш объект       ⇒ учитываем (True)
    Таким образом Alembic не трогает системные таблицы PostGIS.
    """
    if reflected and compare_to is None:
        return False
    return True
# ───────────────────────────────────────────────────────────────────


def run_migrations_online() -> None:
    """Запускает миграции в online-режиме (через прямое подключение)."""
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
            include_schemas=True,     # видеть схему объекта важно
        )

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
