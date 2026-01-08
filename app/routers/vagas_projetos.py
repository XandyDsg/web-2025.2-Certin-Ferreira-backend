from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.database.database import get_db
from app.models.vagas_projetos import VagaProjeto
from app.models.usuario import Usuario
from app.schemas.vagas_projetos import VagaBase

router = APIRouter(
    prefix="/vagas",
    tags=["vagas"]
)
@router.post("/")
def criar_vaga(
    request: VagaBase,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)  # depois ligamos ao auth
):
    if usuario.tipo != "professor":
        raise HTTPException(
            status_code=403,
            detail="Apenas professores podem criar vagas"
        )

    projeto = db.query(Projetos).filter(
        Projetos.id == request.projeto_id,
        Projetos.professor_usuario_id == usuario.id
    ).first()

    if not projeto:
        raise HTTPException(
            status_code=404,
            detail="Projeto não encontrado ou não pertence ao professor"
        )

    vaga = vagas_projetos(**request.dict())
    db.add(vaga)
    db.commit()
    db.refresh(vaga)

    return vaga

@router.put("/{vaga_id}")
def editar_vaga(
    vaga_id: int,
    request: VagaBase,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends()
):
    vaga = db.query(vagas_projetos).get(vaga_id)

    if not vaga:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")

    projeto = db.query(Projetos).get(vaga.projeto_id)

    if projeto.professor_usuario_id != usuario.id:
        raise HTTPException(
            status_code=403,
            detail="Você não pode editar esta vaga"
        )

    for campo, valor in request.dict().items():
        setattr(vaga, campo, valor)

    db.commit()
    db.refresh(vaga)

    return vaga

@router.get("/projeto/{projeto_id}")
def listar_vagas_por_projeto(
    projeto_id: int,
    db: Session = Depends(get_db)
):
    vagas = db.query(vagas_projetos).filter(
        vagas_projetos.projeto_id == projeto_id
    ).all()

    return vagas

 
