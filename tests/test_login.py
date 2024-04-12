import pytest
import json
from app import app

# Define test users data
test_users = {
    'user1': 'password1',  # Add more test users if needed
}

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_valid_login(client):
    # Test valid login credentials
    response = client.post('/logi', data={'username': 'hello', 'password': 'goodbye'}, follow_redirects=True)
    assert response.status_code == 200
    # assert b'Welcome, user1' in response.data

def test_invalid_login(client):
    # Test invalid login credentials
    response = client.post('/logi', data={'username': 'hello', 'password': 'goodbye'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid username or password' in response.data

def test_missing_fields(client):
    # Test missing fields
    response = client.post('/logi', data={}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Username and password are required' in response.data

def test_field_length(client):
    # Test field length
    username = 'a' * 51
    password = 'b' * 51
    response = client.post('/logi', data={'username': username, 'password': password}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Username and password must be less than 50 characters long' in response.data

def test_field_types(client):
    # Test field types
    response = client.post('/logi', data={'username': 123, 'password': 456}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Username and password must be strings' in response.data
