from typing import Optional

from pydantic import EmailStr
from sqlmodel import SQLModel


class BaseUser(SQLModel):
    name: str
    email: EmailStr


class CreateUser(BaseUser):
    password: str


class UpdateUser(BaseUser):
    old_password: str
    new_password: Optional[str] = None


class CurrentUser(BaseUser):
    id: int
