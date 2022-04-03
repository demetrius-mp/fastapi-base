from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    email: EmailStr = Field(
        nullable=False,
    )
    password: str = Field(nullable=False)


class CreateUser(SQLModel):
    name: str
    email: EmailStr
    password: str


class CurrentUser(SQLModel):
    name: str
    email: EmailStr
