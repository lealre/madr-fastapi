from fastapi import APIRouter

from src.database import T_Session
from src.schemas import AuthorList, AuthorPublic, AuthorSchema, Message
from src.security import CurrentUser

router = APIRouter(prefix='/author', tags=['author'])


@router.post('/', response_model=AuthorPublic)
def add_author(
    author: AuthorSchema, session: T_Session, user: CurrentUser
): ...


@router.delete('/{auhtor_id}', response_model=Message)
def delete_author(author_id: int, session: T_Session, user: CurrentUser): ...


@router.patch('/{auhtor_id}', response_model=AuthorPublic)
def update_author(
    author_id: int, author: AuthorSchema, session: T_Session, user: CurrentUser
): ...


@router.get('/{auhtor_id}', response_model=AuthorList)
def get_author_by_id(author_id: int, session: T_Session): ...


@router.get('/', response_class=AuthorList)
def get_author_with_name_like(name: str, session: T_Session): ...
