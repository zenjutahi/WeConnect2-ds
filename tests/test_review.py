import unittest
import os
import json
import sys
import inspect

from .data import ( review_data, review_null_data)

from app import create_app


class BusinessReviewTestCase(unittest.TestCase):

    """This class initializes the app with test data for review"""

    def setUp(self):
        self.app = create_app(config_name="testing")
        self.app = self.app.test_client()


    def post_review_exist(self,data):
        res = self.app.post(
            "/api/businesses/{}/reviews".format(2),
            data=json.dumps(data),
            content_type="application/json")
        return res

    def post_review_non_exist(self,data):
        res = self.app.post(
            "/api/businesses/{}/reviews".format(8),
            data=json.dumps(data),
            content_type="application/json")
        return res

    def test_review_can_only_be_done_to_existing_business(self):
        """ user can only review an existing business"""
        response = self.post_review_non_exist(review_data)

        self.assertEqual(response.status_code, 409)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("existing business", response_msg["message"])

    def test_user_can_review_a_business(self):
        """ user can only review an existing business"""
        response = self.post_review_exist(review_data)
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("successfully created a review", response_msg["message"])

    def test_getAllReviews_only_done_to_existing_business(self):
        """ user can only review an existing business"""
        response = self.app.get("/api/businesses/{}/reviews".format(8))
        self.assertEqual(response.status_code, 409)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Enter a registred business", response_msg["message"])

    def test_check_review_input_ensure_not_null(self):
        """ check user can not input null review"""
        response = self.post_review_exist(review_null_data)
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("You have to enter a review value", response_msg["message"])

    def test_geta_all_reviews_for_a_business(self):
        """ user can get all reviews to a business"""
        response = self.app.get("/api/businesses/{}/reviews".format(2),)
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("reviews succesfully retreaved", response_msg["message"])


if __name__ == "__main__":
    unittest.main()
