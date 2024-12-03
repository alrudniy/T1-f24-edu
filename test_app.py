import unittest
from app import app, db_session, User  # Import necessary components from your app
from flask import Flask, session
from werkzeug.security import generate_password_hash
from flask_login import LoginManager, login_user, current_user

class TestLogin(unittest.TestCase):

    def setUp(self):
        """Set up a test client and add a test user to the database."""
        self.app = app.test_client()  # Create a test client for the Flask app
        self.app.testing = True # propagate exceptions
        # Add a test user (ensure this user doesn't already exist)
        hashed_password = generate_password_hash("testpassword", method='scrypt')
        test_user = User(username="testuser", password=hashed_password, firstname="Test", lastname="User")
        db_session.add(test_user)
        db_session.commit()
        self.test_user_id = test_user.id # get the id of the test user

    def tearDown(self):
        """Clean up the test user after the test."""
        user = db_session.get(User, self.test_user_id)
        if user:
            db_session.delete(user)
            db_session.commit()

    def test_invalid_login(self):
        """Test login with invalid credentials."""
        # Simulate a login request with incorrect password
        response = self.app.post('/', data={'username': 'testuser', 'password': 'wrongpassword'}, follow_redirects=True)
        # Check for flash message indicating invalid credentials
        self.assertIn(b'Invalid username or password', response.data)
        # Check that the user is not logged in
        with self.app.session_transaction() as sess:
            self.assertNotIn('user_id', sess) # check user_id is not in session

    def test_valid_login(self):
        """Test login with valid credentials."""
        # Simulate a login request with correct credentials
        response = self.app.post('/', data={'username': 'testuser', 'password': 'testpassword'}, follow_redirects=True)
        # Check that the user is redirected to the pick_a_path page
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'pick_a_path', response.data)
        # Check that the user is logged in (using current_user)
        with self.app.test_request_context('/'): # Needed for current_user to work
            self.assertTrue(current_user.is_authenticated)


if __name__ == '__main__':
    unittest.main()
