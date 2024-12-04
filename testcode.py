import unittest
from flask import Flask
from your_flask_app import app, db_session, User

class SurveyFormTestCase(unittest.TestCase):
    def setUp(self):
        """Set up the test client and any required test data."""
        self.app = app.test_client()
        self.app.testing = True

        # Create a test user for authentication
        self.test_username = 'testuser'
        self.test_password = 'testpassword'
        hashed_password = User.hash_password(self.test_password)  # Use your hash function
        test_user = User(username=self.test_username, password=hashed_password)
        db_session.add(test_user)
        db_session.commit()

    def tearDown(self):
        """Clean up database."""
        db_session.query(User).filter_by(username=self.test_username).delete()
        db_session.commit()

    def login(self):
        """Helper method to log in."""
        return self.app.post(
            '/',
            data={'username': self.test_username, 'password': self.test_password},
            follow_redirects=True,
        )

    def test_survey_page_access(self):
        """Test that the survey page is accessible after login."""
        self.login()
        response = self.app.get('/survey')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Survey', response.data)

    def test_survey_form_submission(self):
        """Test form submission and validate the server's response."""
        self.login()
        response = self.app.post(
            '/survey',
            data={
                'name': 'John Doe',
                'email': 'johndoe@example.com',
                'age': '18-27',
                'gender': 'male',
                'feedback': 'Great website!',
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Thank you for your feedback', response.data)  # Adjust based on your success message

if __name__ == '__main__':
    unittest.main()
