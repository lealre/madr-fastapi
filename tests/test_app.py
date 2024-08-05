from http import HTTPStatus


def test_read_home_root(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Root Endpoint!'}
