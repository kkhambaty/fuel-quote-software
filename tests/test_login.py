import unittest
from app import app
from login.login import users

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_login_page_loads(self):
        response = self.app.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_successful_login(self):
        response = self.app.post('/login/', data=dict(username='user1', password='password1'), follow_redirects=True)
        self.assertIn(b'Hello, user1', response.data)

    def test_unsuccessful_login(self):
        response = self.app.post('/login/', data=dict(username='user1', password='wrong_password'), follow_redirects=True)
        self.assertIn(b'Invalid username or password.', response.data)

    def test_logout(self):
        with self.app as c:
            with c.session_transaction() as sess:
                sess['logged_in'] = True
                sess['username'] = 'user1'
            response = c.get('/login/logout', follow_redirects=True)
            self.assertNotIn(b'user1', response.data)
            self.assertNotIn(b'Hello', response.data)
            self.assertNotIn(b'Logout', response.data)
            self.assertIn(b'Welcome to the site', response.data)

if __name__ == '__main__':
    unittest.main()
