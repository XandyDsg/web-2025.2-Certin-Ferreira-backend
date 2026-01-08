from typing import List, Union
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, field_validator
from pathlib import Path

# Pega o caminho da pasta raiz onde está o .env
BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    API_PREFIX: str = "/api"
    DEBUG: bool = False
    DATABASE_URL: str  = "sqlite:///./test.db" # Sem valor padrão para forçar a leitura do .env
    ALLOWED_ORIGINS: List = []

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def assemble_allowed_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        return v

    # ESTA LINHA ABAIXO PRECISA DE EXATAMENTE 4 ESPAÇOS (OU 1 TAB)
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=True
    )

settings = Settings()

try:
    settings = Settings()
    print("Configurações carregadas com sucesso!")
except Exception as e:
    print(f"Erro ao carregar configurações: {e}")
   
