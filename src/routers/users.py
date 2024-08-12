from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from src.database import T_Session
from src.models import User
from src.schemas.base import Message
from src.schemas.users import UserPublic, UserSchema
from src.security import CurrentUser, get_password_hash

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', response_model=UserPublic, status_code=HTTPStatus.CREATED)
def create_user(user: UserSchema, session: T_Session):
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

    hashed_password = get_password_hash(user.password)

    user_db = User(
        username=user.username, email=user.email, password=hashed_password
    )

    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    return user_db


@router.put('/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserSchema,
    session: T_Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions.'
        )

    hashed_password = get_password_hash(user.password)

    current_user.username = user.username
    current_user.email = user.email
    current_user.password = hashed_password

    session.commit()
    session.refresh(current_user)

    return current_user


@router.delete('/{user_id}', response_model=Message)
def delete_user(
    user_id: int,
    session: T_Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions.'
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'User Deleted.'}
