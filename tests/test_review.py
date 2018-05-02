import unittest
import os
import json
import sys
import inspect

from .my_data import ( review_data, review_null_data, user_login_data, user_login_data2)

from app import create_app


class BusinessReviewTestCase(unittest.TestCase):

    """This class initializes the app with test data for review"""

    def setUp(self):
        self.app = create_app(config_name="testing")
        self.app = self.app.test_client()
        self.login = self.post_data_login(user_login_data)
        self.login2 = self.post_data_login(user_login_data2)
        self.data = json.loads(self.login.get_data(as_text=True))

        self.data2= json.loads(self.login2.get_data(as_text=True))

        self.token2 = self.data2['token']
        self.token = self.data['token']

    def post_review_exist(self,data):
        res = self.app.post(
            "/api/businesses/{}/reviews".format(2),
            data=json.dumps(data),headers= {
                "Content-Type": "application/json",
                "Authorization": 'Bearer ' + self.token})
        return res

    def post_review(self,data):
        res = self.app.post(
            "/api/businesses/{}/reviews".format(2),
            data=json.dumps(data),headers= {
                "Content-Type": "application/json",
                "Authorization": 'Bearer ' + self.token2})
        return res

    def post_review_non_exist(self,data):
        res = self.app.post(
            "/api/businesses/{}/reviews".format(8),
            data=json.dumps(data),headers= {
                "Content-Type": "application/json",
                "Authorization": 'Bearer ' + self.token})
        return res

    def post_data_login(self, data):
        res = self.app.post(
            "/api/auth/login",
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
        response = self.post_review(review_data)
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("successfully created a review", response_msg["message"])

    def test_getAllReviews_only_done_to_existing_business(self):
        """ user can only review an existing business"""
        response = self.app.get("/api/businesses/{}/reviews".format(8), headers=
                {"Authorization": 'Bearer ' + self.token})
        self.assertEqual(response.status_code, 409)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Enter a registred business", response_msg["message"])

    def test_check_user_can_not_review_own_business(self):
        """ check user can not review their own business"""
        response = self.post_review_exist(review_data)
        self.assertEqual(response.status_code, 403)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("can not review your own business", response_msg["message"])

    def test_check_review_input_ensure_not_null(self):
        """ check user can not input null review"""
        response = self.post_review(review_null_data)
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("You have to enter a review value", response_msg["message"])

    def test_geta_all_reviews_for_a_business(self):
        """ user can get all reviews to a business"""
        response = self.app.get("/api/businesses/{}/reviews".format(2),headers=
                {"Authorization": 'Bearer ' + self.token})
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("reviews succesfully retreaved", response_msg["message"])


if __name__ == "__main__":
    unittest.main()
