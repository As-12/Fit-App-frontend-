import os
os.environ['ENV'] = "test"

import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from main import app

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
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_invalid_url(self):
        response = self.client().get('/invalid', follow_redirects=True)
        self.assertEqual(response.status_code, 404)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
