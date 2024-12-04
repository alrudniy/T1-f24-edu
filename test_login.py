import unittest
import os
from app import app, db_session, User  # Import necessary items from app.py
from werkzeug.security import generate_password_hash
from flask import url_for

class TestLogin(unittest.TestCase):

    def setUp(self):
        # Set up a test client and test database
        app.config['TESTING'] = True  # Important for testing!
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection for testing
        self.app = app.test_client()
        # Create a test user (if needed)
        hashed_password = generate_password_hash('testpassword', method='scrypt')
        test_user = User(username='testuser', password=hashed_password, firstname='Test', lastname='User')
        db_session.add(test_user)
        db_session.commit()

    def tearDown(self):
        # Clean up the test database after each test
        db_session.rollback() # Discard any changes made during the test
        db_session.query(User).filter_by(username='testuser').delete() # Remove the test user
        db_session.commit()
        db_session.close()

    def test_empty_login(self):
        response = self.app.post(url_for('login'), data={'username': '', 'password': ''}, follow_redirects=True)
        self.assertIn(b'Invalid username or password', response.data)

    def test_valid_login(self):
        response = self.app.post(url_for('login'), data={'username': 'testuser', 'password': 'testpassword'},
follow_redirects=True)
        self.assertIn(b'Pick a Path', response.data) # Check for successful redirect

    def test_invalid_username(self):
        response = self.app.post(url_for('login'), data={'username': 'invaliduser', 'password': 'testpassword'},
follow_redirects=True)
        self.assertIn(b'Invalid username or password', response.data)

    def test_invalid_password(self):
        response = self.app.post(url_for('login'), data={'username': 'testuser', 'password': 'wrongpassword'},
follow_redirects=True)
        self.assertIn(b'Invalid username or password', response.data)
                                                                                                                         
if __name__ == '__main__':
    unittest.main()
