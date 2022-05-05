from __future__ import annotations

from fastapi import Depends
from prisma import Client

from src.core.security import decode_jwt, oauth2_scheme

from .http_exceptions import credentials_exception

database = Client()


async def get_db():
    if not database.is_connected():
        await database.connect()

    return database


async def get_current_user(
    db: Client = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    token_data = decode_jwt(token)
    if token_data is None or token_data.email is None:
        raise credentials_exception

    user = await db.user.find_unique(
        where={
            "email": token_data.email,
        },
    )

    if user is None:
        raise credentials_exception

    return user
