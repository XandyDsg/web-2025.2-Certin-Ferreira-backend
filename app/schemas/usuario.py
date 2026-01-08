from typing import Optional, Dict, List
from datetime import datetime
from pydantic import BaseModel

class UsuarioBase(BaseModel):
    nome: str
    email: str
    descricao: Optional[str] = None
    curso: Optional[str] = None
    instituicao: Optional[str] = None
    semestre: Optional[int] = None

class UsuarioCreate(UsuarioBase):
    senha: str

class UsuarioResponse(UsuarioBase):
    id: int
    perfil_foto: Optional[str] = None

    class Config:
        from_attributes = True

class UsuarioInformacoes(BaseModel):
    perfil_foto: Optional[str] = None
    formacoes: Optional[List[Dict[str, str]]] = []
    idiomas: Optional[List[Dict[str, str]]] = []
    niveis: Optional[List[Dict[str, str]]] = []



