from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlmodel import Session

from src.core import security
from src.core.dependencies import get_current_user, get_db
from src.core.http_exceptions import credentials_exception
from src.repository.user import check_user_credentials, create_user, get_user_by_email
from src.schemas.user import CreateUser, CurrentUser

auth_router = APIRouter(prefix="/auth", tags=["authentication"])


@auth_router.post("/sign-up", response_model=CurrentUser)
async def sign_up(user: CreateUser, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user.email)

    if existing_user is not None:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail="This email is already being used.",
        )

    created_user = create_user(db, user_data=user)

    db.add(created_user)
    db.commit()
    db.refresh(created_user)

    return created_user


@auth_router.post("/sign-in", response_model=security.Token)
async def sign_in(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = check_user_credentials(db, form_data.username, form_data.password)
    if user is None:
        raise credentials_exception

    access_token = security.create_access_token(email=user.email)

    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/me", response_model=CurrentUser)
async def get_self(current_user: CurrentUser = Depends(get_current_user)):
    return current_user
