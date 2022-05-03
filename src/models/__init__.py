from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


# define your database tables (models) here
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    name: str = Field(nullable=False)
    email: EmailStr = Field(
        nullable=False,
    )
    password: str = Field(nullable=False)
