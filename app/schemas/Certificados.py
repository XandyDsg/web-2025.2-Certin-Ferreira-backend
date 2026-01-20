from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


# -------- BASE --------
class CertificadoBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    keywords: Optional[List[str]] = None

class CertificadoCreate(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    data_criacao: datetime
    keywords: Optional[List[str]] = None


# -------- UPDATE --------
class CertificadoUpdate(BaseModel):
    nome_certificado: Optional[str] = None
    descricao: Optional[str] = None
    keywords: Optional[List[str]] = None
    status: Optional[str] = None
    error: Optional[str] = None
    completed_at: Optional[datetime] = None


# -------- RESPONSE --------
class CertificadoResponse(CertificadoCreate):
    id: int
    status: str
    created_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True

class CertificadoPublico(BaseModel):
    id: int
    titulo: str
    descricao: str | None
    data_criacao: str

    class Config:
        from_attributes = True
