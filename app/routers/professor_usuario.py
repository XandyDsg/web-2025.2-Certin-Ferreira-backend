from fastapi import APIRouter, Depends, HTTPException, status
from app.database.database import get_session
from app.core.security import get_current_user
from app.models.usuario import Usuario
from app.schemas.professor_usuario import ProfessorUsuarioUpdate
from sqlmodel import Session, select
from app.core.security import get_password_hash, verify_password, create_access_token

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.post("/completar-perfil")
def completar_perfil(data: ProfessorUsuarioUpdate, usuario_atual: Usuario = Depends(get_current_user)):
    pass