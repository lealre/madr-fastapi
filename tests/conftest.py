import factory
import factory.fuzzy
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from src.app import app
from src.database import get_session
from src.models import Author, Book, User, table_registry
from src.security import get_password_hash


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test_name_{n}')
    email = factory.LazyAttribute(lambda user: f'{user.username}@test.com')
    password = factory.LazyAttribute(lambda user: f'{user.username}_pass')


class BookFactory(factory.Factory):
    class Meta:
        model = Book

    year = factory.fuzzy.FuzzyInteger(1, 2000)
    title = factory.Sequence(lambda n: f'book_{n}')
    author_id = 1


class AuthorFactory(factory.Factory):
    class Meta:
        model = Author

    name = factory.Sequence(lambda n: f'author_{n}')


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:16', driver='psycopg') as postgres:
        _engine = create_engine(postgres.get_connection_url())

        with _engine.begin():
            yield _engine


@pytest.fixture
def session(engine):
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
        session.rollback()

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']


@pytest.fixture
def user(session):
    pwd = 'testest'

    user = UserFactory(password=get_password_hash(pwd))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = pwd  # Monkey Patch

    return user


@pytest.fixture
def other_user(session):
    user = UserFactory()

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@pytest.fixture
def author(session):
    author = AuthorFactory()

    session.add(author)
    session.commit()
    session.refresh(author)

    return author


@pytest.fixture
def book(session, author):
    book = BookFactory()

    session.add(book)
    session.commit()
    session.refresh(book)

    return book
