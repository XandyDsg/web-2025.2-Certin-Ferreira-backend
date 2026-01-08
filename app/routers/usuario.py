from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioResponse # Certifique-se de ter esses schemas
from app.core.security import get_password_hash

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.post("/", response_model=UsuarioResponse)
def cadastrar_usuario(request: UsuarioCreate, db: Session = Depends(get_db)):
    # 1. Verifica se o e-mail já existe
    usuario_existente = db.query(Usuario).filter(Usuario.email == request.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Este e-mail já está cadastrado")

    # 2. Cria o novo usuário com a senha criptografada
    novo_usuario = Usuario(
        nome=request.nome,
        email=request.email,
        tipo=request.tipo, # ex: "aluno" ou "professor"
        senha=get_password_hash(request.senha) # <--- AQUI ESTÁ O SEGREDO
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario