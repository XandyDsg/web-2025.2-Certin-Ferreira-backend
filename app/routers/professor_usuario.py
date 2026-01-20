from fastapi import APIRouter, Depends, HTTPException
from app.database.database import get_session
from app.core.security import get_current_user
from app.models.usuario import Usuario
from app.schemas.professor_usuario import ProfessorUsuarioUpdate
from sqlmodel import Session, select
from app.core.security import get_password_hash, verify_password, create_access_token

router = APIRouter(tags=["Professor"])

@router.post("/professor/completar-perfil")
def completar_perfil_professor(
    data: ProfessorUsuarioUpdate,
    session: Session = Depends(get_session),
    usuario: Usuario = Depends(get_current_user)
):
    if usuario.tipo != "professor":
        raise HTTPException(
            status_code=403,
            detail="Apenas professores podem acessar esta rota"
        )

    for campo, valor in data.dict(exclude_unset=True).items():
        setattr(usuario, campo, valor)

    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    return {"message": "Perfil do professor atualizado com sucesso"}
