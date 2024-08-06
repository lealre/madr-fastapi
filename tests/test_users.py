from http import HTTPStatus

from src.schemas import UserPublic


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'testname',
            'email': 'test@test.com',
            'password': 'testpass',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'testname',
        'email': 'test@test.com',
        'id': 1,
    }


def test_create_user_with_duplicated_username(client, user):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': 'different@email.com',
            'password': 'testpass',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists.'}


def test_create_user_with_duplicated_email(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'different_username',
            'email': user.email,
            'password': 'testpass',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists.'}


def test_get_all_users_empty(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_get_all_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_get_user_by_id(client, user):
    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': user.username,
        'email': user.email,
    }


def test_get_user_by_id_not_found(client, user):
    response = client.get('/users/555')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found.'}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'update_name',
            'email': 'update@email.com',
            'password': 'update_password',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'update_name',
        'email': 'update@email.com',
        'id': user.id,
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User Deleted.'}
