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


class UserBusinessTestCase(unittest.TestCase):

    """This class initializes the app with test data for business"""

    def setUp(self):
        self.app = create_app(config_name="testing")
        self.app = self.app.test_client()
        self.app.post(
            "/api/businesses",
            data=json.dumps(
                dict(
                    name="A2z ICT Company",
                    description="We Will Do Basic Web Functionalities In Django And Flask",
                    location="Nairobi")),
            content_type="application/json")

    def test_business_registration(self):
        """ Test API can register a a business"""
        response = self.app.post(
            "/api/businesses",
            data=json.dumps(
                dict(
                    name="A2z ICT Company Kenya",
                    description="We Will Do Basic Web Functionalities In Django And Flask",
                    location="Nairobi")),
            content_type="application/json")

        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("created", response_msg["message"])

    def test_if_business_already_registered(self):
        """ Test API can check a registered business"""
        response = self.app.post(
            "/api/businesses",
            data=json.dumps(
                dict(
                    name="A2z ICT Company Kenya",
                    description="We Will Do Basic Web Functionalities In Django And Flask.",
                    location="Nairobi")),
            content_type="application/json")

        self.assertEqual(response.status_code, 409)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("already registered", response_msg["message"])

    def test_user_entred_name_and_location_data(self):
        """ Check user entred name and location to register business"""
        response = self.app.post(
            "/api/businesses",
            data=json.dumps(
                dict(
                    name="",
                    description="We Will Do Basic Web Functionalities In Django And Flask.",
                    location="")),
            content_type="application/json")

        self.assertEqual(response.status_code, 403)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("business name and location", response_msg["message"])

    def test_user_can_get_all_businesses(self):
        """ Test user can retreave all busineses"""
        response = self.app.get("/api/businesses")

        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("These are all the businesses", response_msg["message1"])

    def test_user_can_delete_business_based_on_its_ID(self):
        """ Test user can delete business with its Id """
        response = self.app.delete("/api/businesses/{}".format(1))

        self.assertEqual(response.status_code, 202)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("deleted", response_msg["message"])

    def test_user_can_edit_business_based_on_ID(self):
        """ User can edit business based on its ID"""
        initial_data = self.app.post(
            "/api/businesses",
            data=json.dumps(
                dict(
                    name="A2z ICT Company Kenya",
                    description="We Will Do Basic Web Functionalities In Django And Flask.",
                    location="Nairobi")),
            content_type="application/json")
        response = self.app.put(
            "/api/businesses/{}".format(2),
            data=json.dumps(
                dict(
                    name="Andela kenya",
                    description="Here you simply own your own",
                    location="RoySambu")),
            content_type="application/json")

        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Edited", response_msg["message"])

    def test_user_edited__name_and_location_and_entred_data(self):
        """ Check user entred name and location to register business"""
        response = self.app.put(
            "/api/businesses/{}".format(2),
            data=json.dumps(
                dict(
                    name="",
                    description="We Will Do Basic Web Functionalities In Django And Flask.",
                    location="")),
            content_type="application/json")

        self.assertEqual(response.status_code, 403)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Business name and Location", response_msg["message"])

    def test_if_user_can_get_business_using_ID(self):
        """Test if user can get business using Id"""
        response = self.app.get("/api/businesses/{}".format(2))

        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Here is the searched business", response_msg["message"])

    # def test_check_if_only_Logged_user_can_register(self):
    #     """ Check if user can register without logging in """
    #     response = self.app.put("/api/businesses/{}".format(2),
    #                       data=json.dumps(dict(name="Andela kenya", description="Here you simply own your own",
    #                                       location="RoySambu")), content_type="application/json")
    #     self.assertEqual(response.status_code, 404)
    #     response_msg = json.loads(response.data.decode("UTF-8"))
    #     self.assertIn("You need to log in", response_msg["message"])


if __name__ == "__main__":
    unittest.main()
