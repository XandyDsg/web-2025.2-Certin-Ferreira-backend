from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import relationship
from app.database.database import Base
from sqlmodel import SQLModel, Field

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha = Column(String, nullable=False)
    tipo = Column(String, nullable=False)  # "aluno" | "professor"

    # -------- PERFIL --------
    descricao = Column(String, nullable=True)
    curso = Column(String, nullable=True)
    instituicao = Column(String, nullable=True)
    semestre = Column(Integer, nullable=True)

    # -------- EXTRAS (APENAS ALUNO) --------
    # Armazenados como JSON
    formacoes = Column(JSON, nullable=True, default=list)
    idiomas = Column(JSON, nullable=True, default=list)

    # -------- RELACIONAMENTOS --------
    certificados = relationship(
        "Certificado",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )

