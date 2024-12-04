import unittest
from app import app # Import your Flask app instance

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_invalid_login(self):
        response = self.app.post("/", data={"username": "invalid_user", "password": "wrong_password"})
        self.assertEqual(response.status_code, 401) # Or check for a redirect to login with an error parameter
        # You can also check for specific content in the response if needed
