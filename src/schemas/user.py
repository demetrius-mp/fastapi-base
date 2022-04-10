from pydantic import EmailStr
from sqlmodel import SQLModel


class CreateUser(SQLModel):
    name: str
    email: EmailStr
    password: str


class CurrentUser(SQLModel):
    name: str
    email: EmailStr
