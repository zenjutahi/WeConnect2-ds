import unittest
import os
import json
import sys
# import inspect

# currentdir = os.path.dirname(os.path.abspath(
#   inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(currentdir)
# sys.path.insert(0, parentdir)

from app import create_app



class UserStuffTestCase(unittest.TestCase):
    
    """This class initializes the app with test data"""
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.app = app.test_client()
        self.app.post("/auth/register",
                    data=json.dumps(dict(email="jeff@gmail.com",username="jefftest",
                                password="jeffpass")), content_type="application/json")

        self.app.post("/auth/login",
                        data=json.dumps(dict(email="jeff@gmail.com",usename="jefftest",
                                        password="jeffpass")), content_type="application/json")

    def test_user_registration(self):
        """ Test API can register a user"""
        response = self.app.post("/auth/register",
                       data=json.dumps(dict(email="jeff@gmail.com",username="jefftest",
                         password="jeffpass")), content_type="application/json")

        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("registered", response_msg["Message"])
        


if __name__ == "__main__":
   unittest.main()