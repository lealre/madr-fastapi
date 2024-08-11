from http import HTTPStatus

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from sqlalchemy import select

from src.database import T_Session
from src.models import Author
from src.schemas import AuthorList, AuthorPublic, AuthorSchema, Message
from src.security import CurrentUser

router = APIRouter(prefix='/author', tags=['author'])


@router.post('/', response_model=AuthorPublic)
def add_author(
    author: AuthorSchema, session: T_Session, user: CurrentUser
): 
    author_db = session.scalar(select(Author).where(Author.name == author.name))

    if author_db:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'{author.name} already in MADR.'
        )
    
    author_db = Author(**author.model_dump())

    session.add(author_db)
    session.commit()
    session.refresh(author_db)

    return author_db


# @router.delete('/{auhtor_id}', response_model=Message)
# def delete_author(author_id: int, session: T_Session, user: CurrentUser): ...


# @router.patch('/{auhtor_id}', response_model=AuthorPublic)
# def update_author(
#     author_id: int, author: AuthorSchema, session: T_Session, user: CurrentUser
# ): ...


@router.get('/{auhtor_id}', response_model=AuthorPublic)
def get_author_by_id(author_id: int, session: T_Session):

    author_db = session.scalar(select(Author).where(Author.id == author_id))

    if not author_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail= 'Author not found in MADR.'
        )
    
    return author_db

# @router.get('/', response_class=AuthorList)
# def get_author_with_name_like(name: str, session: T_Session): ...
