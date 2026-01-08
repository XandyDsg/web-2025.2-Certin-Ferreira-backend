from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.database.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    perfil_foto = Column(String, nullable=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha = Column(String, nullable=False)

    descricao = Column(String, nullable=True)
    curso = Column(String, nullable=True)
    instituicao = Column(String, nullable=True)
    semestre = Column(Integer, nullable=True)

    certificados = relationship(
        "Certificado",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )

