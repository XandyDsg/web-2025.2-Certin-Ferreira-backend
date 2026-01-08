from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.professor_usuario import ProfessorUsuarioBase
from app.models.professor_usuario import ProfessorUsuario

router = APIRouter(
    prefix="/professor",
    tags=["professor"]
)

@router.post("/create")
def create_professor(
    request: ProfessorUsuarioBase,
    db: Session = Depends(get_db)
):
    professor = Professor(**request.dict())
    db.add(professor)
    db.commit()
    db.refresh(professor)
    return professor

