import pytest
import json
from app import app

# Define test user data
TEST_USERNAME = 'test_user'
TEST_PASSWORD = 'test_password'

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database for testing
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Create a test user in the database
            user = User(username=TEST_USERNAME, password=TEST_PASSWORD)
            db.session.add(user)
            db.session.commit()
        yield client
        # Clean up: Drop all tables after testing
        db.drop_all()

def test_valid_login(client):
    # Test valid login credentials
    response = client.post('/logi', data={'username': TEST_USERNAME, 'password': TEST_PASSWORD}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome, user1' in response.data

def test_invalid_login(client):
    # Test invalid login credentials
    response = client.post('/logi', data={'username': TEST_USERNAME, 'password': 'wrong_password'}, follow_redirects=True)
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
