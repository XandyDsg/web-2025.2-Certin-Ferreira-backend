from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.database import Base

class Certificado(Base):
    __tablename__ = "certificados"

    id = Column(Integer, primary_key=True, index=True)

    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=True)

    data_criacao = Column(DateTime, default=datetime.utcnow)

    status = Column(String, default="pendente")
    error = Column(String, nullable=True)

    keywords = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    usuario = relationship(
        "Usuario",
        back_populates="certificados"
    )
