from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# читаем .env в корне репо
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://radar:radar@postgres:5432/radar",
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, future=True)

Base = declarative_base()
