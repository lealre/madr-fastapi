from http import HTTPStatus

from tests.conftest import BookFactory


def test_add_book(client, token):
    response = client.post(
        '/book',
        headers={'Authorization': f'Bearer {token}'},
        json={'year': 2024, 'title': 'book title', 'author_id': 1},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'year': 2024,
        'title': 'book title',
        'author_id': 1,
    }


def test_add_book_already_exists(client, token, book):
    response = client.post(
        '/book',
        headers={'Authorization': f'Bearer {token}'},
        json={'year': 2024, 'title': book.title, 'author_id': 1},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': f'{book.title} already in MADR.'}


def test_delete_book(client, token, book):
    response = client.delete(
        f'/book/{book.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Book deleted from MADR.'}


def test_delete_book_not_found(client, token, book):
    response = client.delete(
        f'/book/{10}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Book not found in MADR.'}


def test_patch_book(session, client, token):
    input_year = 2000
    book = BookFactory(year=input_year)

    session.add(book)
    session.commit()

    year_expected = 2024

    assert book.year == input_year

    response = client.patch(
        f'/book/{book.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'year': year_expected},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': book.id,
        'year': year_expected,
        'title': book.title,
        'author_id': book.author_id,
    }


def test_patch_book_not_found(client, token, book):
    response = client.patch(
        f'/book/{10}',
        headers={'Authorization': f'Bearer {token}'},
        json={'year': 2000},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Book not found in MADR.'}


def test_get_book_by_id(client, book):
    response = client.get(f'/book/{book.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': book.id,
        'year': book.year,
        'title': book.title,
        'author_id': book.author_id,
    }


def test_get_book_by_id_not_found(client, book):
    response = client.get(f'/book/{10}')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Book not found in MADR.'}
