from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.database.database import get_session, get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioLogin, UsuarioCreate, UsuarioResponse, UsuarioUpdate, UsuarioPublico, UsuarioFormacao, UsuarioIdioma
from sqlmodel import Session, select
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.security import get_current_user

router = APIRouter(tags=["Usuários"])

@router.post("/login")
def login(data: UsuarioLogin, session: Session = Depends(get_session)):
    # Busca qualquer usuário pelo e-mail (seja professor ou aluno)
    user = session.exec(select(Usuario).where(Usuario.email == data.email)).first()
    
    # Verifica a senha comparando o que veio do front com o 'user.senha' do banco
    if not user or not verify_password(data.senha, user.senha):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Credenciais inválidas")

    # O segredo: o token leva o 'tipo' (professor/estudante) para o React saber o que fazer
    token = create_access_token({
        "sub": user.email, 
        "user_id": user.id, 
        "tipo": user.tipo
    })
    return {"access_token": token, "token_type": "bearer"}

@router.post("/signup")
def signup(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    existe = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if existe:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=get_password_hash(usuario.senha),
        tipo=usuario.tipo
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return {"detail": "Usuário criado com sucesso"}



@router.get("/me", response_model=UsuarioResponse)
def me(user: Usuario = Depends(get_current_user)):
    return user


@router.put("/me", response_model=UsuarioResponse)
def atualizar_usuario(
    data: UsuarioUpdate,
    session: Session = Depends(get_session),
    user: Usuario = Depends(get_current_user)
):
    # Professores não podem ter extras
    if user.tipo == "professor":
        data.formacoes = None
        data.idiomas = None

    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(user, campo, valor)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user

@router.get("/me/formacoes", response_model=list[UsuarioFormacao])
def listar_formacoes(
    user: Usuario = Depends(get_current_user)
):
    if user.tipo == "professor":
        return []
    return user.formacoes or []


@router.get("/me/idiomas", response_model=list[UsuarioIdioma])
def listar_idiomas(
    user: Usuario = Depends(get_current_user)
):
    if user.tipo == "professor":
        return []
    return user.idiomas or []


@router.get("/buscar", response_model=list[UsuarioPublico])
def buscar_usuarios(
    q: str = Query(..., min_length=2),
    session: Session = Depends(get_session),
    user: Usuario = Depends(get_current_user)
):
    resultados = session.exec(
        select(Usuario)
        .where(Usuario.nome.ilike(f"%{q}%"))
        .limit(10)
    ).all()

    return resultados
