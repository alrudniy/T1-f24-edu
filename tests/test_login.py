import unittest
from app import app # corrected import
from flask import url_for # added import


class TestLoginFormValidation(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()


    def tearDown(self):
        self.app_context.pop()  # No need for db_session management here as it's handled by the app context

    def test_empty_fields(self):
        response = self.app.post(url_for('login'), data={'username': '', 'password': ''}, follow_redirects=True)
        self.assertIn(b'Invalid username or password', response.data)

    def test_invalid_username(self):
        # If you have specific username format requirements, test them here
        # For example, if usernames must be alphanumeric:
        response = self.app.post(url_for('login'), data={'username': 'invalid username!', 'password': 'password'}, follow_redirects=True)
        self.assertIn(b'Invalid username or password', response.data)  # Assuming incorrect username leads to a general login failure message

    def test_invalid_password(self):
        # If you have password requirements (e.g., min length), test them here.
        # For this example, I'm assuming any incorrect password will trigger the general error message.
        response = self.app.post(url_for('login'), data={'username': 'testuser', 'password': 'wrongpassword'}, follow_redirects=True)
        self.assertIn(b'Invalid username or password', response.data)

    # Add more tests for other validation rules as needed

if __name__ == '__main__':
    unittest.main()
