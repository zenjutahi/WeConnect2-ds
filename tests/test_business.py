import unittest
import os
import json
import sys
import inspect

from .my_data import ( business_orig_data, business_register_data,
                     business_register_duplicate, business_data_blank,
                     business_edit_data, user_login_data)

from app import create_app


class UserBusinessTestCase(unittest.TestCase):

    """This class initializes the app with test data for business"""

    def setUp(self):
        self.app = create_app(config_name="testing")
        self.app = self.app.test_client()
        self.login = self.post_data_login(user_login_data)
        self.data = json.loads(self.login.get_data(as_text=True))

        self.token = self.data['token']
        self.post_business_register(business_orig_data)

    def post_business_register(self,data):
        res = self.app.post(
            "/api/businesses",
            data=json.dumps(data),headers= {
                "Content-Type": "application/json",
                "Authorization": 'Bearer ' + self.token}
                )
        return res

    def post_business_edit(self, data):
        res = self.app.put(
            "/api/businesses/{}".format(2),
            data=json.dumps(data),headers= {
                "Content-Type": "application/json",
                "Authorization": 'Bearer ' + self.token}
                )
        return res

    def post_data_login(self, data):
        res = self.app.post(
            "/api/auth/login",
            data=json.dumps(data),
            content_type="application/json")
        return res

    def test_business_registration(self):
        """ Check API can register a business"""
        response = self.post_business_register(business_register_data)

        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("created", response_msg["message"])

    def test_if_business_already_registered(self):
        """ Check if business already registered"""
        response = self.post_business_register(business_register_duplicate)

        self.assertEqual(response.status_code, 409)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("already registered", response_msg["message"])

    def test_user_entred_name_and_location_data(self):
        """ Check user entred name and location to register business"""
        response = self.post_business_register(business_data_blank)

        self.assertEqual(response.status_code, 403)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("business name and location", response_msg["message"])

    def test_user_can_get_all_businesses(self):
        """ Test user can retreave all busineses"""
        response = self.app.get("/api/businesses",headers=
                {"Authorization": 'Bearer ' + self.token})

        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("These are all the businesses", response_msg["message1"])

    def test_user_can_delete_business_based_on_its_ID(self):
        """ Test user can delete business with its Id """
        response = self.app.delete("/api/businesses/{}".format(1), headers=
                {"Authorization": 'Bearer ' + self.token})

        self.assertEqual(response.status_code, 202)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("deleted", response_msg["message"])

    def test_user_can_only_access_existing_business(self):
        """ Test user can delete business with its Id """
        response = self.app.get("/api/businesses/{}".format(12), headers=
                {"Authorization": 'Bearer ' + self.token})

        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Bussniess does not exist", response_msg["message"])

    def test_user_can_edit_business_based_on_ID(self):
        """ User can edit business based on its ID"""
        response = self.post_business_edit(business_edit_data)

        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("edited", response_msg["message"])

    def test_user_can_not_edit_with_blank_data(self):
        """ Check user entred name and location to register business"""
        response = self.post_business_edit(business_data_blank)

        self.assertEqual(response.status_code, 403)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Business name and Location", response_msg["message"])

    def test_if_user_can_get_business_using_ID(self):
        """Test if user can get business using Id"""
        response = self.app.get("/api/businesses/{}".format(2), headers=
                {"Authorization": 'Bearer ' + self.token})

        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Here is the searched business", response_msg["message"])


if __name__ == "__main__":
    unittest.main()
