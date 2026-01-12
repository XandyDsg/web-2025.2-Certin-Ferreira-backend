from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.database.database import get_db
from app.models.vagas_projetos import VagaProjeto, Projeto  # Nomes de classe corrigidos
from app.models.usuario import Usuario
from app.schemas.vagas_projetos import VagaBase

router = APIRouter(
    tags=["vagas"]
)

@router.post("/")
def criar_vaga(
    request: VagaBase,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):
    # 1. Verifica se é professor
    if usuario.tipo != "professor":
        raise HTTPException(
            status_code=403,
            detail="Apenas professores podem criar vagas"
        )

    # 2. Busca o Projeto (Certifique-se que o campo no banco é professor_id)
    # Corrigido de 'Projetos' para 'Projeto'
    projeto = db.query(Projeto).filter(
        Projeto.id == request.projeto_id,
        Projeto.professor_id == usuario.id 
    ).first()

    if not projeto:
        raise HTTPException(
            status_code=404,
            detail="Projeto não encontrado ou não pertence a você"
        )

    # 3. Cria a vaga usando a classe correta VagaProjeto
    # Corrigido de 'vagas_projetos' para 'VagaProjeto'
    vaga = VagaProjeto(**request.model_dump()) 
    db.add(vaga)
    db.commit()
    db.refresh(vaga)

    return vaga

@router.put("/{vaga_id}")
def editar_vaga(
    vaga_id: int,
    request: VagaBase,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user) # Adicionado o porteiro aqui também
):
    vaga = db.query(VagaProjeto).filter(VagaProjeto.id == vaga_id).first()

    if not vaga:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")

    # Verifica se o projeto da vaga pertence ao professor logado
    projeto = db.query(Projeto).filter(Projeto.id == vaga.projeto_id).first()

    if projeto.professor_id != usuario.id:
        raise HTTPException(
            status_code=403,
            detail="Você não tem permissão para editar vagas deste projeto"
        )

    # Atualiza os campos
    for campo, valor in request.model_dump().items():
        setattr(vaga, campo, valor)

    db.commit()
    db.refresh(vaga)

    return vaga

@router.get("/projeto/{projeto_id}")
def listar_vagas_por_projeto(
    projeto_id: int,
    db: Session = Depends(get_db)
):
    vagas = db.query(VagaProjeto).filter(
        VagaProjeto.projeto_id == projeto_id
    ).all()

    return vagas