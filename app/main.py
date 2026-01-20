from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import engine, Base
from app.routers import usuario, Certificados, professor_usuario, vagas_projetos
# Removido import duplicado de Certificados

app = FastAPI(title="Certin API", description="Api para o aplicativo de controle de certificados mais rápido do mundo!")

@app.get("/")
def home():
    return {"message": "API do Certin rodando com sucesso!", "docs": "/docs"}
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://front-end-certin-app.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Registros sem o prefixo complexo para bater com seu Frontend atual

app.include_router(usuario.router, prefix="/usuarios")
app.include_router(Certificados.router, prefix="/certificados")
app.include_router(professor_usuario.router, prefix="/professores")
app.include_router(vagas_projetos.router, prefix="/vagas")
