import unittest
import os
import json
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from app import create_app


class BusinessReviewTestCase(unittest.TestCase):

    """This class initializes the app with test data for review"""

    def setUp(self):
        self.app = create_app(config_name="testing")
        self.app = self.app.test_client()
        self.app.post(
            "/api/businesses{}".format(2),
            data=json.dumps(
                dict(
                    business_id=2,
                    value="I love it",
                    comments="I love it more")),
            content_type="application/json")

    def test_review_can_only_be_done_to_existing_business(self):
        """ user can only review an existing business"""
        response = self.app.post(
            "/api/businesses/{}/reviews".format(8),
            data=json.dumps(
                dict(
                    business_id=8,
                    value="I love it",
                    comments="I love it more")),
            content_type="application/json")
        self.assertEqual(response.status_code, 409)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("existing business", response_msg["message"])

    def test_getAllReviews_only_done_to_existing_business(self):
        """ user can only review an existing business"""
        response = self.app.get("/api/businesses/{}/reviews".format(8))
        self.assertEqual(response.status_code, 409)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Enter a registred business", response_msg["message"])

    # def test_check_review_input_ensure_not_null(self):
    #     """ check user can not input null review"""
    #     response = self.app.post("/api/businesses/{}/reviews".format(1),
    #                 data=json.dumps(dict(business_id=1,value="",
    #                                         comments = "")),content_type="application/json")
    #     self.assertEqual(response.status_code, 400)
    #     response_msg = json.loads(response.data.decode("UTF-8"))
    #     self.assertIn("You have to enter a review value", response_msg["message"])

    # def test_geta_all_reviews_for_a_business(self):
    #     """ user can get all reviews to a business"""
    #     response = self.app.get("/api/businesses/{}/reviews".format(1),)
    #     self.assertEqual(response.status_code, 201)
    #     response_msg = json.loads(response.data.decode("UTF-8"))
    #     self.assertIn("reviews succesfully retreaved", response_msg["message"])


if __name__ == "__main__":
    unittest.main()
