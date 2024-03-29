import pytest
import json
from app import app

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_valid_login(self):
        # Test valid login credentials
        response = self.app.post('/login', json={'username': 'user1', 'password': 'password1'})
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Login successful')

    def test_invalid_login(self):
        # Test invalid login credentials
        response = self.app.post('/login', json={'username': 'user1', 'password': 'wrongpassword'})
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['error'], 'Invalid username or password')

    def test_missing_fields(self):
        # Test missing fields
        response = self.app.post('/login', json={})
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 'Username and password are required')

    def test_field_length(self):
        # Test field length
        username = 'a' * 51
        password = 'b' * 51
        response = self.app.post('/login', json={'username': username, 'password': password})
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 'Username and password must be less than 50 characters long')

    def test_field_types(self):
        # Test field types
        response = self.app.post('/login', json={'username': 123, 'password': 456})
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 'Username and password must be strings')

if __name__ == '__main__':
    pytest.main()