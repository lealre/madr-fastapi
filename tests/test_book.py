from http import HTTPStatus

from tests.conftest import BookFactory


def test_add_book(client, token, author):
    response = client.post(
        '/book',
        headers={'Authorization': f'Bearer {token}'},
        json={'year': 2024, 'title': 'book title', 'author_id': 1},
    )

    assert response.status_code == HTTPStatus.CREATED
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


def test_add_book_author_id_not_found(client, token):
    book = BookFactory()
    response = client.post(
        '/book',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'year': book.year,
            'title': book.title,
            'author_id': book.author_id,
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        'detail': f'Author with ID {book.author_id} not found.'
    }


def test_add_book_not_authenticated(client):
    response = client.post(
        '/book',
        json={'year': 2024, 'title': 'book title', 'author_id': 1},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


def test_book_title_sanitization_schema(client, token, author):
    expected_title = 'a title to correct'
    response = client.post(
        '/book',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'year': 2024,
            'title': ' A   TitLE  to correct     ',
            'author_id': 1,
        },
    )

    assert response.json()['title'] == expected_title


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


def test_delete_book_not_authenticated(client, book):
    response = client.delete(f'/book/{book.id}')

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


def test_patch_book(session, client, token, author):
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


def test_patch_book_not_authenticated(client, book):
    response = client.patch(f'/book/{10}', json={'year': 2000})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


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


def test_list_books_empty(client):
    response = client.get('/book')

    assert response.json()['books'] == []


def test_list_books_filter_name_should_return_5_books(client, session, author):
    expected_books = 5
    session.bulk_save_objects(BookFactory.create_batch(5))
    books_with_title = BookFactory.create_batch(5, title='title')
    for n, book in enumerate(books_with_title):
        book.title = f'title_{n}'
    session.bulk_save_objects(books_with_title)
    session.commit()

    response = client.get('/book/?name=oo')

    assert len(response.json()['books']) == expected_books


def test_list_books_filter_name_should_return_empty(client, session, author):
    session.bulk_save_objects(BookFactory.create_batch(5))
    session.commit()

    response = client.get('/book/?name=title')

    assert response.json()['books'] == []


def test_list_books_filter_year_should_return_5_books(client, session, author):
    expected_books = 5
    session.bulk_save_objects(BookFactory.create_batch(5, year=2000))
    session.bulk_save_objects(BookFactory.create_batch(5, year=2024))
    session.commit()

    response = client.get('/book/?year=2000')

    assert len(response.json()['books']) == expected_books


def test_list_books_filter_year_should_return_empty(client, session, author):
    session.bulk_save_objects(BookFactory.create_batch(5, year=2000))
    session.commit()

    response = client.get('/book/?year=2024')

    assert response.json()['books'] == []


def test_list_books_filter_combined_should_return_5_books(
    session, client, author
):
    expected_books = 5
    books = BookFactory.create_batch(7, year=2000)
    books[-1].title = 'title'
    books[0].year = 2024
    session.bulk_save_objects(books)
    session.commit()

    response = client.get('/book/?year=2000&name=oo')

    assert len(response.json()['books']) == expected_books


def test_list_books_pagination_should_return_20_books(session, client, author):
    expected_books = 20
    session.bulk_save_objects(BookFactory.create_batch(25, year=2000))
    session.commit()

    response = client.get('/book/?title=2000')

    assert len(response.json()['books']) == expected_books
