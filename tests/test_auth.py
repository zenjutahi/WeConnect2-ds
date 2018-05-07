import unittest
import os
import json
import sys
import inspect
from .my_data import ( user_data2, user_data3, user_data, user_login_data,
                    user_login_wrong_password, user_data_key_nul_login,reset_password_data_wrong,
                    user_login_not_registred,user_data_blank,update_password_data,
                    user_login_blank, user_data_key_nul_register, reset_password_data )

from app import create_app


class UserAuthTestCase(unittest.TestCase):

    """This class initializes the app with test data"""

    def setUp(self):
        self.app = create_app(config_name="testing")
        self.app = self.app.test_client()
        self.post_data_register(user_data)

        self.login = self.post_data_login(user_login_data)
        self.data = json.loads(self.login.get_data(as_text=True))

        self.token = self.data['token']

    def post_data_register(self,data):
        res = self.app.post(
            "/api/auth/register",
            data=json.dumps(data),
            content_type="application/json")
        return res

    def post_none_json_data_register(self,data):
        res = self.app.post(
            "/api/auth/register",
            data=json.dumps(data),
            content_type="text/plain")
        return res

    def post_data_login(self, data):
        res = self.app.post(
            "/api/auth/login",
            data=json.dumps(data),
            content_type="application/json")
        return res

    def post_data_reset_password(self, data):
        res = self.app.post(
            "/api/auth/reset-password",
            data=json.dumps(data),
            content_type="application/json")
        return res

    def post_non_json_data_login(self, data):
        res = self.app.post(
            "/api/auth/login",
            data=json.dumps(data),
            content_type="text/plain")
        return res

    def post_non_json_data_reset_password(self, data):
        res = self.app.post(
            "/api/auth/reset-password",
            data=json.dumps(data),
            content_type="text/plain")
        return res

    def post_data_password_update(self, data):
        res = self.app.post(
            "/api/auth/reset-password/update",
            data=json.dumps(data),
            headers={
                "Content-Type": "application/json",
                "Authorization": 'Bearer ' + self.token})
        return res

    def post_non_json_data_password_update(self, data):
        res = self.app.post(
            "/api/auth/reset-password/update",
            data=json.dumps(data),
            headers={
                "content_type":'text/plain',
                "Authorization": 'Bearer ' + self.token})
        return res


    def test_user_registration(self):
        """ Test API can register a user"""
        response = self.post_data_register(user_data2)

        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("created", response_msg["message"])

    def test_user_filled_all_required_keys_to_register(self):
        """ Test API ensures user filled required keys"""
        response = self.post_data_register(user_data_key_nul_register)

        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("is Missing", response_msg["message"])

    def test_user_registration_data_is_json(self):
        """ Test API can only accept json data"""
        response = self.post_none_json_data_register(user_data2)

        self.assertEqual(response.status_code, 405)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Request should be JSON format", response_msg["message"])

    def test_user_used_valid_email(self):
        """ Test API checks for valid email"""
        response = self.post_data_register(user_data3)

        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Enter valid email to register", response_msg["message"])

    def test_user_used_valid_email_reset_password(self):
        """ Test API checks for valid email to reset password"""
        response = self.post_data_reset_password(reset_password_data_wrong)

        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Not registered email", response_msg["message"])

    def test_user_used_can_reset_password(self):
        """ Test API enables user to reset password"""
        response = self.post_data_reset_password(reset_password_data)

        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Use this token to reset password", response_msg["message"])

    def test_user_needs_access_token_to_change_password(self):
        """ Test API enables user to update password"""
        response = self.post_data_password_update(update_password_data)

        self.assertEqual(response.status_code, 405)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("You need the access token to update password", response_msg["message"])

    def test_user_already_registered(self):
        """ Test API can check a registered user"""
        response = self.post_data_register(user_data)

        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("login instead", response_msg["message"])

    def test_user_login(self):
        """ Test API can login a user"""
        response = self.post_data_login(user_login_data)

        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("valid", response_msg["message"])

    def test_user_filled_all_required_keys_to_login(self):
        """ Test API ensures user filled required keys"""
        response = self.post_data_login(user_data_key_nul_login)

        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("is Missing", response_msg["message"])

    def test_user_login_with_json_data(self):
        """ Test API checks user json data"""
        response = self.post_non_json_data_login(user_login_data)

        self.assertEqual(response.status_code, 405)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Request should be JSON format", response_msg["message"])

    def test_user_reset_password_with_json_data(self):
        """ Test API checks user resets passsword with json data"""
        response = self.post_non_json_data_reset_password(user_login_data)

        self.assertEqual(response.status_code, 405)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Request should be JSON format", response_msg["message"])

    def test_user_password_update_with_json_data(self):
        """ Test API checks user updates passsword with json data"""
        response = self.post_non_json_data_password_update(reset_password_data)

        self.assertEqual(response.status_code, 405)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Request should be JSON format", response_msg["message"])

    def test_user_login_with_wrong_password(self):
        """ Test API can check if user used wrong password"""
        response = self.post_data_login(user_login_wrong_password)

        self.assertEqual(response.status_code, 403)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Wrong", response_msg["message"])

    def test_check_if_user_is_registrerd(self):
        """ Test API can check if user is registered"""
        response = self.post_data_login(user_login_not_registred)

        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Not registered", response_msg["message"])

    def test_if_user_has_logged_out(self):
        """ Test API can check if user is logged out"""
        response = self.app.get(
            "/api/auth/logout",
            headers={
                "Authorization": 'Bearer ' + self.token})
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("logged out", response_msg["message"])

    def test_check_if_user_entered_blank_data_to_register(self):
        """ Test API to check if user entered blank data"""
        response = self.post_data_register(user_data_blank)

        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("email, username and password", response_msg["message"])

    def test_check_if_user_entered_blank_data_to_reset_password(self):
        """ Test API to check if user entered blank data to reset password"""
        response = self.post_data_reset_password(user_data_blank)

        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("your email to reset password", response_msg["message"])

    def test_check_if_user_entered_blank_data_to_login(self):
        """ Test API to check if user entered blank data"""
        response = self.post_data_login(user_login_blank)

        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("both password and username", response_msg["message"])


if __name__ == "__main__":
    unittest.main()
