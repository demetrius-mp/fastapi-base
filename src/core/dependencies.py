from __future__ import annotations

from fastapi import Depends
from sqlmodel import Session, select

from src.core.security import decode_jwt, oauth2_scheme
from src.database import engine
from src.models import User

from .http_exceptions import credentials_exception


# exported
def get_db():
    with Session(engine) as session:
        yield session


# exported
def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    token_data = decode_jwt(token)
    if token_data is None or token_data.email is None:
        raise credentials_exception

    stmt = select(User).where(User.email == token_data.email)

    return db.exec(stmt).first()
