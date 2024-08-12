from http import HTTPStatus

from tests.conftest import AuthorFactory


def test_add_author(client, token):
    response = client.post(
        '/author',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'test-name'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'id': 1, 'name': 'test-name'}


def test_add_author_already_exists(client, token, author):
    response = client.post(
        '/author',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': author.name},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': f'{author.name} already in MADR.'}


def test_add_author_not_authenticated(client):
    response = client.post(
        '/author',
        json={'name': 'test'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


def test_delete_author(client, token, author):
    response = client.delete(
        f'/author/{author.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Author deleted from MADR.'}


def test_delete_author_not_found(client, token, author):
    response = client.delete(
        '/author/555',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Author not found in MADR.'}


def test_delete_author_not_authenticated(client, author):
    response = client.delete(f'/author/{author.id}')

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


def test_update_author(client, token, author):
    expected_name = 'name updated'
    response = client.patch(
        f'/author/{author.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': expected_name},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': author.id, 'name': expected_name}


def test_update_author_not_found(client, token, author):
    response = client.patch(
        '/author/555',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'update'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Author not found in MADR.'}


def test_update_author_not_authenticated(client, author):
    response = client.patch(
        '/author/555',
        json={'name': 'update'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


def test_get_author_by_id(client, author):
    response = client.get(f'/author/{author.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': author.id, 'name': author.name}


def test_get_author_by_id_not_found(client, author):
    response = client.get('/author/555')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Author not found in MADR.'}


def test_list_authors_filter_name_should_return_5_authors(client, session):
    expected_authors = 5
    session.bulk_save_objects(AuthorFactory.create_batch(5))
    author_with_name = AuthorFactory.create_batch(5, name='name')
    for n, book in enumerate(author_with_name):
        book.title = f'name_{n}'
    session.commit()

    response = client.get('/author/?name=author')

    assert len(response.json()['authors']) == expected_authors


def test_list_authors_filter_name_should_return_empty(client, session):
    session.bulk_save_objects(AuthorFactory.create_batch(5))
    session.commit()

    response = client.get('/author/?name=different name')

    assert response.json()['authors'] == []


def test_list_authors_filter_name_empty(client, session):
    session.bulk_save_objects(AuthorFactory.create_batch(5))
    session.commit()

    response = client.get('/author/?name=')

    assert response.json()['authors'] == []


def test_list_authors_pagination_should_return_20_authors(session, client):
    expected_books = 20
    session.bulk_save_objects(AuthorFactory.create_batch(25))
    session.commit()

    response = client.get('/author/?name=author')

    assert len(response.json()['authors']) == expected_books
