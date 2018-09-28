def test_home(client):
    rv = client.get('/home')
    assert b'hello from Flask!' in rv.data
