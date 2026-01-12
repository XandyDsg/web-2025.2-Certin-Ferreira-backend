from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database.database import get_session
from app.models.usuario import Usuario

# ================= CONFIG =================

SECRET_KEY = "CHAVE_SUPER_SECRETA"  # em produção: variável de ambiente
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 2

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="usuarios/login"
)

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# ================= PASSWORD =================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        raise HTTPException(
            status_code=400,
            detail="Senha muito longa (máx. 72 caracteres)"
        )
    return pwd_context.hash(password)

# ================= TOKEN =================

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

# ================= CURRENT USER =================

def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
) -> Usuario:
    payload = decode_access_token(token)

    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

    user = session.get(Usuario, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado"
        )

    return user
