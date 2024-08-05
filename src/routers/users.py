from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_session
from src.models import User
from src.schemas import Message, UserPublic, UserSchema, UsersList

T_Session = Annotated[Session, Depends(get_session)]


router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', response_model=UserPublic)
def create_user(user: UserSchema, session=Depends(get_session)):
    user_db = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if user_db:
        if user_db.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists.',
            )
        if user_db.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists.',
            )

    user_db = User(
        username=user.username, email=user.email, password=user.password
    )

    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    return user_db


@router.get('/', response_model=UsersList)
def get_all_users(session: T_Session, skip: int = 0, limit: int = 100):
    users_db = session.scalars(select(User).offset(skip).limit(limit))

    return {'users': users_db}


@router.get('/{user_id}', response_model=UserPublic)
def get_user_by_id(user_id: int, session: T_Session):
    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found.',
        )

    return user_db


@router.put('/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema, session: T_Session):
    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found.',
        )

    user_db.username = user.username
    user_db.email = user.email
    user_db.password = user.password

    session.commit()
    session.refresh(user_db)

    return user_db


@router.delete('/{user_id}', response_model=Message)
def delete_user(user_id: int, session: T_Session):
    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found.',
        )

    session.delete(user_db)
    session.commit()

    return {'message': 'User Deleted.'}
