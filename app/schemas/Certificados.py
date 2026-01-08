from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class CertificadoBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    data_criacao: datetime
    keywords: Optional[List[str]] = None

class CertificadoResponse(CertificadoBase):
    id: int
    status: str
    created_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True

class CertificadoCreate(CertificadoBase):
    pass

class CertificadoUpdate(BaseModel):
    status: Optional[str] = None
    error: Optional[str] = None
    completed_at: Optional[datetime] = None
