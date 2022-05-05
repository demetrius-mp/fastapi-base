from typing import Optional

from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    name: str
    email: EmailStr


class CreateUser(BaseUser):
    password: str


class UpdateUser(BaseUser):
    old_password: str
    new_password: Optional[str] = None


class CurrentUser(BaseUser):
    id: str
