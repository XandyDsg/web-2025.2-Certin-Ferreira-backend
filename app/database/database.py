from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
from sqlmodel import SQLModel, create_engine, Session

if not settings.DATABASE_URL:
    raise ValueError("A variável DATABASE_URL não foi carregada. Verifique o arquivo .env")
engine = create_engine(settings.DATABASE_URL)


engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}  # necessário para SQLite
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_session():
    with Session(engine) as session:
        yield session

def create_tables():
    Base.metadata.create_all(bind=engine) 
