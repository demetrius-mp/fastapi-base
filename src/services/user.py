from __future__ import annotations

from sqlmodel import Session, select

from src.models import User
from src.schemas.user import CreateUser
from src.services.auth import check_password_hash, generate_password_hash


def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Finds a user with the given email in the database and returns it.
    Returns None if a user with the email does not exists.
    """
    stmt = select(User).where(User.email == email)

    return db.exec(stmt).first()


def create_user(user_data: CreateUser) -> User:
    """
    Creates a user and returns it.
    """
    password = generate_password_hash(user_data.password)

    created_user = User(name=user_data.name, email=user_data.email, password=password)

    return created_user


def get_user_by_email_and_password(
    db: Session, email: str, password: str
) -> User | None:
    """
    Checks if the given email and password are valid, and returns the user.
    Returns None if the email or password is wrong.
    """
    user = get_user_by_email(db, email)

    if user is None or not check_password_hash(password, user.password):
        return None

    return user
