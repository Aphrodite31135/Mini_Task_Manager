from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import logging

DATABASE_URL = "sqlite:///Day2_SQLAlchemy_CRUD/test.db"

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"   # 메시지만 나오게
)

logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

engine=create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}, 
    echo=False
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False, 
    autoflush=False
)

Base=declarative_base()