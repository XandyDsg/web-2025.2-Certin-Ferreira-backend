from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.security import get_current_user

# Importações corrigidas para usar o caminho absoluto do projeto
from app.database.database import get_db
from app.models.Certificados import Certificado
from app.models.usuario import Usuario
from app.schemas.Certificados import (
    CertificadoCreate,
    CertificadoResponse
)

router = APIRouter(
    prefix="/certificados",
    tags=["certificados"]
)

@router.post("/", response_model=CertificadoResponse)
def criar_certificado(
    request: CertificadoCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user) # <--- O segredo está aqui!
):
    # Verificação de regra de negócio
    if usuario.tipo == "professor":
        raise HTTPException(
            status_code=403,
            detail="Professores não podem criar certificados"
        )

    # Criação da instância usando model_dump() (Pydantic V2)
    certificado = Certificado(
        **request.model_dump(),
        usuario_id=usuario.id
    )

    db.add(certificado)
    db.commit()
    db.refresh(certificado)

    return certificado


@router.get(
    "/usuario/{usuario_id}",
    response_model=List[CertificadoResponse]
)
def listar_certificados_usuario(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    certificados = db.query(Certificado).filter(
        Certificado.usuario_id == usuario_id
    ).all()

    return certificados

@router.put("/{certificado_id}", response_model=CertificadoResponse)
def editar_certificado(
    certificado_id: int,
    request: CertificadoCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends()
):
    # Forma moderna de buscar por ID no SQLAlchemy
    certificado = db.get(Certificado, certificado_id)

    if not certificado:
        raise HTTPException(status_code=404, detail="Certificado não encontrado")

    if certificado.usuario_id != usuario.id:
        raise HTTPException(
            status_code=403,
            detail="Você não pode editar este certificado"
        )

    # Atualização dinâmica dos campos
    for campo, valor in request.model_dump().items():
        setattr(certificado, campo, valor)

    db.commit()
    db.refresh(certificado)

    return certificado

@router.delete("/{certificado_id}")
def deletar_certificado(
    certificado_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends()
):
    certificado = db.get(Certificado, certificado_id)

    if not certificado:
        raise HTTPException(status_code=404, detail="Certificado não encontrado")

    if certificado.usuario_id != usuario.id:
        raise HTTPException(
            status_code=403,
            detail="Você não pode apagar este certificado"
        )

    db.delete(certificado)
    db.commit()

    return {"detail": "Certificado removido com sucesso"}

 