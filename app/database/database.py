from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings

# =====================
# ENGINE
# =====================

if not settings.DATABASE_URL:
    raise ValueError("DATABASE_URL não foi carregada. Verifique o .env")

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}  # necessário para SQLite
)

# =====================
# SESSION
# =====================

def get_session():
    with Session(engine) as session:
        yield session

# =====================
# CREATE TABLES
# =====================

def create_tables():
    SQLModel.metadata.create_all(engine)
