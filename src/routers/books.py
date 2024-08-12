from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from src.database import T_Session
from src.models import Book
from src.schemas.base import Message
from src.schemas.books import BookList, BookPublic, BookSchema, BookUpdate
from src.security import CurrentUser

router = APIRouter(prefix='/book', tags=['book'])


@router.post('/', response_model=BookPublic, status_code=HTTPStatus.CREATED)
def add_book(book: BookSchema, session: T_Session, user: CurrentUser):
    db_book = session.scalar(select(Book).where(book.title == Book.title))

    if db_book:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'{db_book.title} already in MADR.',
        )

    db_book = Book(**book.model_dump())

    session.add(db_book)
    session.commit()
    session.refresh(db_book)

    return db_book


@router.delete('/{book_id}', response_model=Message)
def delete_book(book_id: int, session: T_Session, user: CurrentUser):
    db_book = session.scalar(select(Book).where(Book.id == book_id))

    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Book not found in MADR.'
        )

    session.delete(db_book)
    session.commit()

    return {'message': 'Book deleted from MADR.'}


@router.patch('/{book_id}', response_model=BookPublic)
def update_book(
    book_id: int, book: BookUpdate, session: T_Session, user: CurrentUser
):
    db_book = session.scalar(select(Book).where(Book.id == book_id))

    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Book not found in MADR.'
        )

    db_book.year = book.year

    session.add(db_book)
    session.commit()
    session.refresh(db_book)

    return db_book


@router.get('/{book_id}', response_model=BookPublic)
def get_book_by_id(book_id: int, session: T_Session):
    db_book = session.scalar(select(Book).where(Book.id == book_id))

    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Book not found in MADR.'
        )

    return db_book


@router.get('/', response_model=BookList)
def get_book_like(
    session: T_Session,
    name: str | None = None,
    year: int | None = None,
    limit: int = 20,
    offset: int = 0,
):
    query = select(Book)

    if name:
        query = query.filter(Book.title.contains(name))

    if year:
        query = query.filter(Book.year == year)

    db_books = session.scalars(query.limit(limit).offset(offset)).all()

    return {'books': db_books}
