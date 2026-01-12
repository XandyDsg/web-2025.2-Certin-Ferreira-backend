from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from sqlmodel import select
from app.database.database import get_db, get_session
from app.core.security import get_current_user
from app.models.Certificados import Certificado
from app.models.usuario import Usuario
from app.schemas.Certificados import (
    CertificadoCreate,
    CertificadoResponse
)

router = APIRouter(
    tags=["Certificados"]
)

# =========================
# LISTAR CERTIFICADOS DO USUÁRIO LOGADO
# =========================
@router.get("/me", response_model=List[CertificadoResponse])
def listar_meus_certificados(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    certificados = db.query(Certificado).filter(
        Certificado.usuario_id == current_user.id
    ).all()

    return certificados

# =========================
# CRIAR CERTIFICADO
# =========================
@router.post("/criar/me", response_model=CertificadoResponse, status_code=201)
def criar_certificado(
    data: CertificadoCreate,
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user)
):
    if user.tipo == "professor":
        raise HTTPException(
            status_code=403,
            detail="Professores não podem criar certificados"
        )

    certificado = Certificado(
        **data.model_dump(),
        usuario_id=user.id
    )

    db.add(certificado)
    db.commit()
    db.refresh(certificado)

    return certificado


# =========================
# Visualizar Certificados
# =========================

@router.get("/{id}", response_model=CertificadoResponse)
def get_certificado(id: int, session: Session = Depends(get_session)):
    cert = session.get(Certificado, id)
    if not cert:
        raise HTTPException(status_code=404, detail="Certificado não encontrado")
    return cert

# =========================
# DELETAR CERTIFICADO
# =========================
@router.delete("/{certificado_id}", status_code=204)
def deletar_certificado(
    certificado_id: int,
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user)
):
    certificado = db.get(Certificado, certificado_id)

    if not certificado:
        raise HTTPException(404, "Certificado não encontrado")

    if certificado.usuario_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="Você não pode apagar este certificado"
        )

    db.delete(certificado)
    db.commit()

