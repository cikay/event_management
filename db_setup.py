import os


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import settings

POSTGRES_USER = settings.postgres_user
POSTGRES_PASSWORD = settings.postgres_password
POSTGRES_SERVER = settings.postgres_server
POSTGRES_PORT = settings.postgres_port
POSTGRES_DB = settings.postgres_db


SQLALCHEMY_DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}\
@{POSTGRES_SERVER}/{POSTGRES_DB}'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={}, future=True)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, future=True
)


Base = declarative_base()


# DB Utilities
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
