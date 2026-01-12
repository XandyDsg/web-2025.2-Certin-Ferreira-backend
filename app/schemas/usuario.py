from typing import Optional, List
from pydantic import BaseModel, EmailStr


# ---------- SUB-OBJETOS (JSON) ----------

class UsuarioFormacao(BaseModel):
    curso: str
    instituicao: str
    ano: str


class UsuarioIdioma(BaseModel):
    idioma: str
    nivel: str


# ---------- BASE ----------

class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    descricao: Optional[str] = None
    curso: Optional[str] = None
    instituicao: Optional[str] = None
    semestre: Optional[int] = None


# ---------- CREATE / LOGIN ----------

class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    tipo: str  # "aluno" | "professor"


class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str


# ---------- UPDATE ----------

class UsuarioUpdate(BaseModel):
    descricao: Optional[str] = None
    curso: Optional[str] = None
    instituicao: Optional[str] = None
    semestre: Optional[int] = None
    formacoes: Optional[List[UsuarioFormacao]] = None
    idiomas: Optional[List[UsuarioIdioma]] = None


# ---------- RESPONSE ----------

class UsuarioResponse(UsuarioBase):
    id: int
    tipo: str
    formacoes: List[UsuarioFormacao] = []
    idiomas: List[UsuarioIdioma] = []

    class Config:
        from_attributes = True

class UsuarioPublico(BaseModel):
    id: int
    nome: str
    descricao: str | None
    curso: str | None
    instituicao: str | None
    semestre: int | None
    formacoes: list[dict] = []
    idiomas: list[dict] = []

    class Config:
        from_attributes = True
