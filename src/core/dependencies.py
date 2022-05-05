from __future__ import annotations

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select

from src.database import engine
from src.models import User
from src.services.auth import decode_jwt

from .http_exceptions import credentials_exception


def get_db():
    with Session(engine) as session:
        yield session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/sign-in")


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    token_data = decode_jwt(token)
    if token_data is None or token_data.email is None:
        raise credentials_exception

    stmt = select(User).where(User.email == token_data.email)

    user = db.exec(stmt).first()

    if user is None:
        raise credentials_exception

    return user
