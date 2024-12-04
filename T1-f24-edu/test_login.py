import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # Add parent directory to path

from app import app, db_session, engine  # Import necessary components from app.py

class TestLogin(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True  # Set testing mode
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection for testing
        self.app = app.test_client()  # Create a test client
        # Any database setup required for testing can be done here, but bypassed due to the check in app.py

    def tearDown(self):
        # Any database teardown required for testing can be done here, but bypassed due to the check in app.py
        pass

    def test_empty_username_password(self):
        response = self.app.post('/', data=dict(username='', password=''), follow_redirects=True)
        self.assertIn(b'Invalid username or password', response.data)

    def test_empty_username(self):
        response = self.app.post('/', data=dict(username='', password='test'), follow_redirects=True)
        self.assertIn(b'Invalid username or password', response.data)

    def test_empty_password(self):
        response = self.app.post('/', data=dict(username='test', password=''), follow_redirects=True)
        self.assertIn(b'Invalid username. Must be at least 3 characters.', response.data)

    def test_short_username(self):
        response = self.app.post('/', data=dict(username='ab', password='test123456'), follow_redirects=True)
        self.assertIn(b'Invalid username. Must be at least 3 characters.', response.data)

    def test_empty_password(self):
        response = self.app.post('/', data=dict(username='testuser', password=''), follow_redirects=True)
        self.assertIn(b'Invalid password. Must be at least 6 characters.', response.data)

    def test_short_password(self):
        response = self.app.post('/', data=dict(username='testuser', password='12345'), follow_redirects=True)
        self.assertIn(b'Invalid password. Must be at least 6 characters.', response.data)


if __name__ == '__main__':
    unittest.main()
