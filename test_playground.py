import pytest

import playground


@pytest.fixture
def client():
    app = playground.create_app()
    client = app.test_client()
    yield client


def test_index(client):
    rv = client.get('/')
    assert b'hello from Flask!' in rv.data
