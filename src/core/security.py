from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from src.settings import settings

# exported
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/sign-in")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


def check_password_hash(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def generate_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(email: str) -> str:
    """
    Creates a JWT with the subject being the given email.
    """
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {"sub": email, "exp": expire}

    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def decode_jwt(token: str) -> TokenData | None:
    """
    Decodes the JWT, returning a object containing the user email.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    except JWTError:
        return None

    email: str | None = payload.get("sub")
    if email is None:
        return None

    token_data = TokenData(email=email)

    return token_data
