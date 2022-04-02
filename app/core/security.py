from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlmodel import Session, select

from app.models import User
from app.models.user import CreateUser
from app.settings import settings

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


def get_user(db: Session, email: str) -> User | None:
    """
    Finds a user with the given email in the database and returns it.
    Returns None if a user with the email does not exists.
    """
    stmt = select(User).where(User.email == email)

    return db.exec(stmt).first()


def create_user(db: Session, user: CreateUser) -> User | None:
    """
    Creates a user, and returns it.
    Returns None if a user with the same email already exists.
    """
    password = generate_password_hash(user.password)

    existingUser = get_user(db, user.email)
    if existingUser is not None:
        return None

    created_user = User(name=user.name, email=user.email, password=password)

    return created_user


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    """
    Checks if the given email and password are valid, and returns the user.
    Returns None if the email or password is wrong.
    """
    user = get_user(db, email)

    if user is None or not check_password_hash(password, user.password):
        return None

    return user


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
