from pydantic import BaseModel
from typing import Optional

class VagaBase(BaseModel):
    titulo_vaga: str
    descricao_vaga: Optional[str] = None
    requisitos: Optional[str] = None
    beneficios: Optional[str] = None
    projeto_id: int
