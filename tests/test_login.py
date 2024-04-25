import pytest
import json
from app import app, db
from models import User
from werkzeug.security import generate_password_hash


@pytest.fixture
def user():
    new_user = User(username='testuser', password=generate_password_hash('testpass'))
    db.session.add(new_user)
    db.session.commit()

    yield new_user

    db.session.delete(new_user)
    db.session.commit()

def test_valid_login(client, user):
    new_user = user
    client = app.test_client()
    response = client.post('/logi', data={'username': 'testuser', 'password': 'testpass'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome, testuser' in response.data

def test_invalid_login(client, user):
    new_user = user
    client = app.test_client()
    response = client.post('/logi', data={'username': 'testuser', 'password': 'wrong_password'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid username or password' in response.data

def test_missing_fields(client):
    client = app.test_client()
    response = client.post('/logi', data={}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Username and password are required' in response.data

def test_field_length(client):
    client = app.test_client()
    username = 'a' * 51
    password = 'b' * 51
    response = client.post('/logi', data={'username': username, 'password': password}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Username and password must be less than 50 characters long' in response.data

def test_field_types(client):
    # Test field types
    client = app.test_client()
    response = client.post('/logi', data={'username': 123, 'password': 456}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Username and password must be strings' in response.data
