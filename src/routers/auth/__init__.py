from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from prisma import Client
from prisma.models import User

from src.core import security
from src.core.dependencies import get_current_user, get_db
from src.core.http_exceptions import credentials_exception
from src.schemas.user import CreateUser, CurrentUser, UpdateUser

auth_router = APIRouter(prefix="/auth", tags=["authentication"])


@auth_router.post(
    "/sign-up",
    response_model=CurrentUser,
)
async def sign_up(
    user: CreateUser,
    db: Client = Depends(get_db),
):
    existing_user = await db.user.find_unique(
        {
            "email": user.email,
        }
    )

    if existing_user is not None:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail="This email is already being used.",
        )

    hashed_password = security.generate_password_hash(user.password)
    created_user = await db.user.create(
        {
            "email": user.email,
            "name": user.name,
            "password": hashed_password,
        }
    )

    return created_user


@auth_router.post(
    "/sign-in",
    response_model=security.Token,
)
async def sign_in(
    db: Client = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = await db.user.find_unique(
        {
            "email": form_data.username,
        }
    )
    if user is None or not security.check_password_hash(
        form_data.password, user.password
    ):
        raise credentials_exception

    access_token = security.create_access_token(email=user.email)

    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post(
    "/update-profile",
    response_model=CurrentUser,
)
async def update_profile(
    updated_user_data: UpdateUser,
    current_user: CurrentUser = Depends(get_current_user),
    db: Client = Depends(get_db),
):
    user = await db.user.find_unique({"email": current_user.email})

    if user is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Something went wrong, please try again.",
        )

    if not security.check_password_hash(updated_user_data.old_password, user.password):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Password is incorrect.",
        )

    existing_user = await db.user.find_unique(
        {
            "email": updated_user_data.email,
        }
    )

    if current_user.email != updated_user_data.email and existing_user is not None:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail="This email is already being used.",
        )

    user.name = updated_user_data.name
    user.email = updated_user_data.email

    if updated_user_data.new_password is not None:
        user.password = security.generate_password_hash(updated_user_data.new_password)

    updated_user = await db.user.update(
        data={
            "name": user.name,
            "email": user.email,
            "password": user.password,
        },
        where={
            "email": user.email,
        },
    )

    return updated_user


@auth_router.get(
    "/me",
    response_model=CurrentUser,
)
async def get_self(
    current_user: CurrentUser = Depends(get_current_user),
):
    return current_user
