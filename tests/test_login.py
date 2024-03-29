import pytest
import json
from app import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_valid_login(client):
    # Test valid login credentials
    response = client.post('/login', json={'username': 'user1', 'password': 'password1'})
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert data['message'] == 'Login successful'

def test_invalid_login(client):
    # Test invalid login credentials
    response = client.post('/login', json={'username': 'user1', 'password': 'wrongpassword'})
    data = json.loads(response.data.decode())
    assert response.status_code == 401
    assert data['error'] == 'Invalid username or password'

def test_missing_fields(client):
    # Test missing fields
    response = client.post('/login', json={})
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert data['error'] == 'Username and password are required'

def test_field_length(client):
    # Test field length
    username = 'a' * 51
    password = 'b' * 51
    response = client.post('/login', json={'username': username, 'password': password})
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert data['error'] == 'Username and password must be less than 50 characters long'

def test_field_types(client):
    # Test field types
    response = client.post('/login', json={'username': 123, 'password': 456})
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert data['error'] == 'Username and password must be strings'
