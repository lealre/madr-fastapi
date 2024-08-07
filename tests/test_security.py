from http import HTTPStatus

import pytest
from fastapi import HTTPException
from jwt import decode

from src.database import T_Session
from src.security import create_access_token, get_current_user, settings


def test_jwt():
    data = {'sub': 'test@test.com'}
    token = create_access_token(data)

    result = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert result['sub'] == data['sub']
    assert result['exp']


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_token_with_no_user():
    encoded_token = create_access_token(data={})

    with pytest.raises(HTTPException) as excinfo:
        get_current_user(session=T_Session, token=encoded_token)

    assert excinfo.value.status_code == HTTPStatus.UNAUTHORIZED
    assert excinfo.value.detail == 'Could not validate credentials'
