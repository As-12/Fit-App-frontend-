import os
os.environ['ENV'] = "test"

import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from main import app

# JWT_SECRET environment variable should be set to execute the test
AUTH_TOKEN = os.environ['JWT_SECRET']

class FitAppTestSuite(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Global Endpoints
    """

    def test_invalid_url(self):
        response = self.client().get('/invalid', follow_redirects=True)
        self.assertEqual(response.status_code, 404)


    def test_health_endpoint(self):
        response = self.client().get('/health', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    """
    User Endpoints
    """

    """
    GET /users
    """
    def test_get_user(self):
        response = self.client().get('/users', headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
                                     follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_get_user_no_auth(self):
        response = self.client().get('/users', follow_redirects=True)
        self.assertEqual(response.status_code, 401)

    """
    POST /users
    """
    def test_post_user_invalid_weight(self):
        response = self.client().post('/users', headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
                                      follow_redirects=True)
        data = {
            "target_weight": -20,
            "dob": "2020-04-20",
            "city": "string",
            "state": "string"
        }
        response = self.client().post('/users', json=data, headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
                                      follow_redirects=True)
        self.assertEqual(response.status_code, 422)

    def test_post_user(self):
        data = {
            "target_weight": 0,
            "dob": "2020-04-20",
            "city": "string",
            "state": "string"
        }
        response = self.client().post('/users', json=data, headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
                                      follow_redirects=True)
        self.assertEqual(response.status_code, 201)

        # Cannot post same user twice
        response = self.client().post('/users', json=data, headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
                                      follow_redirects=True)
        self.assertEqual(response.status_code, 422)

    def test_post_user_no_auth(self):
        data = {
            "target_weight": 0,
            "dob": "2020-04-20",
            "city": "string",
            "state": "string"
        }
        response = self.client().post('/users', json=data,
                                      follow_redirects=True)
        self.assertEqual(response.status_code, 401)




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
