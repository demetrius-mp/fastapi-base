from datetime import date
from typing import Optional

from pydantic import BaseModel


class BaseInvoice(BaseModel):
    title: str
    amount: float
    description: Optional[str]
    due_date: Optional[date]


class CreateInvoice(BaseInvoice):
    pass


class UpdateInvoice(BaseInvoice):
    pass


class ReadInvoice(BaseInvoice):
    id: int

    class Config:
        orm_mode = True