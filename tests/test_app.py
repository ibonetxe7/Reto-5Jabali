import pytest
from unittest.mock import patch
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_key'
    return app.test_client()


# gahona: verifica que la página login carga bien
def test_login_get(client):
    assert client.get('/login').status_code == 200


# gahona: verifica que un login correcto redirige
@patch('app.mysql')
def test_login_correcto(mock_mysql, client):
    mock_mysql.connection.cursor.return_value.fetchone.return_value = (1, 'Unax', 2)
    r = client.post('/login', data={'email': 'unax@test.com', 'password': '1234'})
    assert r.status_code == 302


# gahona: verifica que un login incorrecto muestra error
@patch('app.mysql')
def test_login_incorrecto(mock_mysql, client):
    mock_mysql.connection.cursor.return_value.fetchone.return_value = None
    r = client.post('/login', data={'email': 'noexiste@test.com', 'password': '1234'})
    assert r.status_code == 200 and 'incorrectos' in r.data.decode()


# gahona: verifica que logout borra la sesión
def test_logout_borra_sesion(client):
    with client as c:
        with c.session_transaction() as sess:
            sess['nombre'] = 'Unax'
        c.get('/logout')
        with c.session_transaction() as sess:
            assert 'nombre' not in sess