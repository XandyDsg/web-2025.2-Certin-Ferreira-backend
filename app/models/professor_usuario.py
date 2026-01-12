from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database.database import Base


class ProfessorUsuario(Base):
    __tablename__ = "professor_usuarios"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True, index=True, nullable=False)
    senha = Column(String, nullable=False)

    nome_professor = Column(String, nullable=False)
    curso_professor = Column(String, nullable=False)
    instituicao = Column(String, nullable=False)
    formacao_tipo = Column(String, nullable=False)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    usuario = relationship("Usuario", back_populates="professor_usuarios")
    projetos = relationship(
        "Projeto",
        back_populates="professor_usuario",
        cascade="all, delete-orphan"
    )

