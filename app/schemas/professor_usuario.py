from typing import Optional, List
from pydantic import BaseModel


class ProfessorUsuarioBase(BaseModel):
    nome_professor: str
    curso_professor: str
    instituicao: str
    formacao_tipo: str

class ProfessorUsuarioCreate(ProfessorUsuarioBase):
    email: str
    senha: str

class ProfessorUsuarioLogin(ProfessorUsuarioBase):
    email: str
    senha: str

class ProfessorUsuarioUpdate(ProfessorUsuarioBase):
    nome_professor: Optional[str] = None
    curso_professor: Optional[str] = None
    instituicao: Optional[str] = None
    formacao_tipo: Optional[str] = None

class ProjetoResumo(BaseModel):
    id: int
    titulo: str

    class Config:
        from_attributes = True

class ProfessorUsuarioResponse(ProfessorUsuarioBase):
    id: int
    email: str
    projetos: List[ProjetoResumo] = []

    class Config:
        from_attributes = True
