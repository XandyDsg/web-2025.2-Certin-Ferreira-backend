from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, Certificados
from app.core.config import settings
from app.routers import (
    usuario,
    Certificados,
    professor_usuario,
    vagas_projetos,
    auth
)

app = FastAPI(
    title="Certin - aplicativo acadêmico",
    description="Aplicativo para gerenciamento acadêmico de estudantes e cursos.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro dos routers
app.include_router(
    usuario.router,
    prefix=settings.API_PREFIX + "/usuarios",
    tags=["Usuários"]
)

app.include_router(
    Certificados.router,
    prefix=settings.API_PREFIX + "/certificados",
    tags=["Certificados"]
)

app.include_router(
    professor_usuario.router,
    prefix=settings.API_PREFIX + "/professores",
    tags=["Professores"]
)

app.include_router(
    vagas_projetos.router,
    prefix=settings.API_PREFIX + "/vagas",
    tags=["Vagas"]
)

app.include_router(
    vagas_projetos.router,
    prefix=settings.API_PREFIX + "/projetos",
    tags=["Projetos"]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
