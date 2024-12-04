import unittest
import app  # Import your Flask app instance
from flask import Flask, session
from flask_login import LoginManager, login_user
from unittest.mock import patch
from flask_testing import TestCase

class TestLogin(TestCase):

    def create_app(self):
        app.app.config['TESTING'] = True
        app.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection for testing
        app.app.secret_key = 'your_secret_key'  # Set a secret key for testing
        return app.app

    def setUp(self):
        self.client = self.app.test_client()

    def test_login_invalid_credentials(self):
        # Test with incorrect password
        response = self.client.post('/', data={'username': 'testuser', 'password': 'wrongpassword'}, follow_redirects=True)
        self.assert_template_used('login.html')  # Check if redirected back to login page
        self.assertIn(b'Invalid username or password', response.data) # Check for the flash message

        # Test with non-existent user
        response = self.client.post('/', data={'username': 'nonexistentuser', 'password': 'password'}, follow_redirects=True)
        self.assert_template_used('login.html')  # Check if redirected back to login page
        self.assertIn(b'Invalid username or password', response.data) # Check for the flash message

if __name__ == '__main__':
    unittest.main()
