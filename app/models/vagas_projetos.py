from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database.database import Base


class VagaProjeto(Base):
    __tablename__ = "vagas_projetos"

    id = Column(Integer, primary_key=True, index=True)

    titulo_vaga = Column(String, nullable=False)
    descricao_vaga = Column(Text, nullable=True)

    requisitos = Column(Text, nullable=True)
    beneficios = Column(Text, nullable=True)

    projeto_id = Column(Integer, ForeignKey("projetos.id"))

    projeto = relationship(
        "Projeto",
        back_populates="vagas"
    )
