from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlmodel import Session

from src.core.dependencies import get_current_user, get_db
from src.core.http_exceptions import credentials_exception
from src.schemas import Token
from src.schemas.user import CreateUser, CurrentUser, UpdateUser
from src.services.auth import (
    check_password_hash,
    create_access_token,
    generate_password_hash,
)
from src.services.user import (
    create_user,
    get_user_by_email,
    get_user_by_email_and_password,
)

auth_router = APIRouter(prefix="/auth", tags=["authentication"])


@auth_router.post(
    "/sign-up",
    response_model=CurrentUser,
)
async def sign_up(
    user: CreateUser,
    db: Session = Depends(get_db),
):
    existing_user = get_user_by_email(db, user.email)

    if existing_user is not None:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail="This email is already being used.",
        )

    created_user = create_user(user_data=user)

    db.add(created_user)
    db.commit()
    db.refresh(created_user)

    return created_user


@auth_router.post(
    "/sign-in",
    response_model=Token,
)
async def sign_in(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = get_user_by_email_and_password(db, form_data.username, form_data.password)
    if user is None:
        raise credentials_exception

    access_token = create_access_token(email=user.email)

    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post(
    "/update-profile",
    response_model=CurrentUser,
)
async def update_profile(
    updated_user_data: UpdateUser,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = get_user_by_email(db, current_user.email)

    if user is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Something went wrong, please try again.",
        )

    if not check_password_hash(updated_user_data.old_password, user.password):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Password is incorrect.",
        )

    existing_user = get_user_by_email(db, updated_user_data.email)

    if current_user.email != updated_user_data.email and existing_user is not None:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail="This email is already being used.",
        )

    user.name = updated_user_data.name
    user.email = updated_user_data.email

    if updated_user_data.new_password is not None:
        user.password = generate_password_hash(updated_user_data.new_password)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@auth_router.get(
    "/me",
    response_model=CurrentUser,
)
async def get_self(
    current_user: CurrentUser = Depends(get_current_user),
):
    return current_user
