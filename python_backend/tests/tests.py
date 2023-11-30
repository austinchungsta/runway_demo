import os
import sys

# for local testing only -- when executing this file directly as main
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import json

from app import app  # Import your Flask app
from models.reviews_model import AppReviews, session

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Test 1: malformed request without any params
    def test_get_reviews_without_params(self):
        response = self.app.get('/get_reviews')
        self.assertEqual(response.status_code, 400)
        self.assertIn('app_id not provided', response.get_data(as_text=True))
    
    # Test 2: malformed request without hours param
    def test_get_reviews_without_hours(self):
        response = self.app.get('/get_reviews?app_id=447188370') # valid app id
        self.assertEqual(response.status_code, 400)
        self.assertIn("hours parameter not provided", response.get_data(as_text=True))
    
    # Test 3: malformed request without id param
    def test_get_reviews_without_id(self):
        response = self.app.get('/get_reviews?hours=200')
        self.assertEqual(response.status_code, 400)
        self.assertIn('app_id not provided', response.get_data(as_text=True))
    
    # Test 4: malformed request without bad time param
    def test_get_reviews_with_bad_time(self):
        # Replace '12345' with a valid app_id for your test
        response = self.app.get('/get_reviews?app_id=447188370&hours=abcd') # valid app id invalid hours
        self.assertEqual(response.status_code, 500)
        # Add more assertions here based on expected response
    
    # Test 5: malformed request without bad id
    def test_get_reviews_with_bad_app_id(self):
        # Replace '12345' with a valid app_id for your test
        response = self.app.get('/get_reviews?app_id=12345&hours=200') # invalid app id
        self.assertEqual(response.status_code, 500)
        # Add more assertions here based on expected response
    
    # Test 6: well formed request
    def test_get_reviews_with_app_id(self):
        # Replace '12345' with a valid app_id for your test
        response = self.app.get('/get_reviews?app_id=447188370&hours=200') # valid app id
        self.assertEqual(response.status_code, 200)
        # Add more assertions here based on expected response

# For silencing purposeful error messages during testing
class SuppressOutputTestRunner(unittest.TextTestRunner):
    def run(self, test):
        with open(os.devnull, 'w') as null_stream:
            original_stdout = sys.stdout
            original_stderr = sys.stderr
            sys.stdout = null_stream
            sys.stderr = null_stream
            result = super(SuppressOutputTestRunner, self).run(test)
            sys.stdout = original_stdout
            sys.stderr = original_stderr
        return result

if __name__ == '__main__':
    unittest.main(testRunner=SuppressOutputTestRunner)