# app/models/vagas_projetos.py
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database.database import Base

class Projeto(Base):
    __tablename__ = "projetos"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descricao = Column(Text)
    professor_id = Column(Integer, ForeignKey("usuarios.id"))
    
    vagas = relationship("VagaProjeto", back_populates="projeto")

class VagaProjeto(Base):
    __tablename__ = "vagas_projetos"
    id = Column(Integer, primary_key=True, index=True)
    titulo_vaga = Column(String, nullable=False)
    projeto_id = Column(Integer, ForeignKey("projetos.id"))
    
    projeto = relationship("Projeto", back_populates="vagas")