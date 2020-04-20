import os
from datetime import datetime

os.environ['ENV'] = "test"

import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from main import app
from main import db
# JWT_SECRET environment variable should be set to execute the test
AUTH_TOKEN = os.environ['JWT_SECRET']
AUTH_SUBJECT = os.environ['JWT_SUB']


class FitAppTestSuite(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        db.drop_all()
        db.create_all()
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
    POST & DELETE /users
    """

    def test_post_user_invalid_weight(self):
        data = {
            "target_weight": -20,
            "dob": "2020-04-20",
            "city": "string",
            "state": "string"
        }
        response = self.client().post('/users', json=data, headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
                                      follow_redirects=True)
        self.assertEqual(response.status_code, 422)

    def test_post_user_bad_dob(self):
        data = {
            "target_weight": 0,
            "dob": "2099-04-20",
            "city": "string",
            "state": "string"
        }
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

    def test_post_and_delete_user(self):
        data = {
            "target_weight": 0,
            "dob": "2000-04-20",
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

        response = self.client().get('/users', headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
                                     follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['count'], 1)

        response = self.client().delete(f'/users/{AUTH_SUBJECT}', headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
                                        follow_redirects=True)
        self.assertEqual(response.status_code, 204)

        response = self.client().delete(f'/users/{AUTH_SUBJECT}', headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
                                        follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    """
    PATCH /users
    """

    def test_patch_user(self):
        data = {
            "target_weight": 0,
            "dob": "2000-04-20",
            "city": "string",
            "state": "string"
        }
        response = self.client().post('/users', json=data, headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
                                      follow_redirects=True)
        self.assertEqual(response.status_code, 201)

        data = {
            "target_weight": 25,
            "dob": "2000-04-20",
            "city": "Grapevine",
            "state": "Texas"
        }
        response = self.client().patch(f'/users/{AUTH_SUBJECT}', json=data,
                                       headers={"Authorization": f"Bearer {AUTH_TOKEN}"}, follow_redirects=True)
        self.assertEqual(response.status_code, 204)

        data = {
            "target_weight": -10,
            "dob": "2000-04-20",
            "city": "Grapevine",
            "state": "Texas"
        }
        response = self.client().patch(f'/users/{AUTH_SUBJECT}', json=data,
                                       headers={"Authorization": f"Bearer {AUTH_TOKEN}"}, follow_redirects=True)

        self.assertEqual(response.status_code, 422)

        data = {
            "target_weight": 10,
            "dob": "2999-04-20",
            "city": "Grapevine",
            "state": "Texas"
        }
        response = self.client().patch(f'/users/{AUTH_SUBJECT}', json=data,
                                       headers={"Authorization": f"Bearer {AUTH_TOKEN}"}, follow_redirects=True)

        self.assertEqual(response.status_code, 422)

        response = self.client().delete(f'/users/{AUTH_SUBJECT}', headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
                                        follow_redirects=True)
        self.assertEqual(response.status_code, 204)

    def test_patch_no_user(self):
        data = {
            "target_weight": 25,
            "dob": "2000-04-20",
            "city": "Grapevine",
            "state": "Texas"
        }
        response = self.client().patch(f'/users/{AUTH_SUBJECT}', json=data,
                                       headers={"Authorization": f"Bearer {AUTH_TOKEN}"}, follow_redirects=True)

        self.assertEqual(response.status_code, 404)

    def test_patch_different_user(self):
        data = {
            "target_weight": 25,
            "dob": "2000-04-20",
            "city": "Grapevine",
            "state": "Texas"
        }
        response = self.client().patch(f'/users/1234', json=data,
                                       headers={"Authorization": f"Bearer {AUTH_TOKEN}"}, follow_redirects=True)

        self.assertEqual(response.status_code, 403)

    """
    GET /progress
    """

    def test_get_all_progress(self):
        response = self.client().get(f'/progress',
                                     headers={"Authorization": f"Bearer {AUTH_TOKEN}"}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.client().get(f'/progress', follow_redirects=True)
        self.assertEqual(response.status_code, 401)

    """
    GET /progress/{id}
    """

    def test_get_progress(self):
        data = {
            "target_weight": 0,
            "dob": "2000-04-20",
            "city": "string",
            "state": "string"
        }
        response = self.client().post('/users', json=data, headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
                                      follow_redirects=True)
        self.assertEqual(response.status_code, 201)

        response = self.client().get(f'/progress/{AUTH_SUBJECT}',
                                     headers={"Authorization": f"Bearer {AUTH_TOKEN}"}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.client().get(f'/progress/1234', follow_redirects=True,
                                     headers={"Authorization": f"Bearer {AUTH_TOKEN}"})
        self.assertEqual(response.status_code, 403)

        response = self.client().get(f'/progress/{AUTH_SUBJECT}', follow_redirects=True)
        self.assertEqual(response.status_code, 401)

        response = self.client().delete(f'/users/{AUTH_SUBJECT}', headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
                                        follow_redirects=True)
        self.assertEqual(response.status_code, 204)

    """
    POST/PATCH /progress/{id}
    """

    def test_post_patch_progress(self):
        data = {
            "target_weight": 0,
            "dob": "2000-04-20",
            "city": "string",
            "state": "string"
        }
        response = self.client().post('/users', json=data, headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
                                      follow_redirects=True)
        self.assertEqual(response.status_code, 201)

        data = {
            "track_date": datetime.today().date().strftime('%Y-%m-%d'),
            "weight": 255,
            "mood": "neutral",
            "diet": "neutral"
        }
        response = self.client().post(f'/progress/{AUTH_SUBJECT}', json=data,
                                      headers={"Authorization": f"Bearer {AUTH_TOKEN}"}, follow_redirects=True)
        self.assertEqual(response.status_code, 201)

        data["weight"] = 500
        response = self.client().patch(f'/progress/{AUTH_SUBJECT}', json=data,
                                       headers={"Authorization": f"Bearer {AUTH_TOKEN}"}, follow_redirects=True)
        self.assertEqual(response.status_code, 204)

        response = self.client().post(f'/progress/1234', follow_redirects=True,
                                      headers={"Authorization": f"Bearer {AUTH_TOKEN}"})
        self.assertEqual(response.status_code, 403)

        response = self.client().patch(f'/progress/{AUTH_SUBJECT}', follow_redirects=True)
        self.assertEqual(response.status_code, 401)

        response = self.client().delete(f'/users/{AUTH_SUBJECT}', headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
                                        follow_redirects=True)
        self.assertEqual(response.status_code, 204)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
