from datetime import date, datetime
from typing import List, Optional

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


# define your database tables (models) here
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    name: str = Field(nullable=False)
    email: EmailStr = Field(
        nullable=False,
    )
    password: str = Field(nullable=False)

    invoices: List["Invoice"] = Relationship(back_populates="user")


class Invoice(SQLModel, table=True):
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    title: str = Field(nullable=False)
    amount: float = Field(nullable=False)
    description: Optional[str] = Field(nullable=True, default=None)
    due_date: Optional[date] = Field(nullable=True, default=None)

    created_at: datetime = Field(default_factory=datetime.utcnow)

    user_id: int = Field(nullable=False, foreign_key="user.id")
    user: User = Relationship(back_populates="invoices")
