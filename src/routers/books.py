from http import HTTPStatus
from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from src.database import T_Session
from src.models import Books 
from src.schemas import BookPublic, BookSchema

router = APIRouter(prefix='/books', tags=['books'])


@router.post('/', response_model=BookPublic)
def add_book(book: BookSchema, session: T_Session):

    db_book = session.scalar(select(Books).where(book.title == Books.title))

    if db_book:
        raise HTTPException(
            status_code= HTTPStatus.BAD_REQUEST,
            detail= f'{db_book.title} already in MADR'
        )
    
    db_book = Books(**book.model_dump())
    
    session.add(db_book)
    session.commit()
    session.refresh(db_book)

    return db_book


@router.delete('/{book_id}')
def delete_book(): ...


@router.patch('/{book_id}')
def update_book(): ...


@router.get('/{book_id}', response_model=BookPublic)
def get_book_by_id(book_id: int, session: T_Session):

    db_book = session.scalar(select(Books).where(Books.id == book_id))

    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail = 'Book not found in MADR'
        )
    
    return db_book


@router.get('/', response_model=BookPublic)
def get_book_like(): ...
