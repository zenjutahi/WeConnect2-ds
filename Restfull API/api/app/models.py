from flask import session, request
from werkzeug.security import generate_password_hash

class User(object):
    """" Here i want to create a user who can login, register a business
     pass review... """

    user_id = 0
    users = {}

    def __init__(self, email, username, password):
        """ Contructors to initialize class """

        User.user_id += 1
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)

    def create_user(self):
        """ Class to create and store a user object """
        self.users.update({
            self.user_id: {
                'email': self.email,
                'username': self.username,
                'password':self.password
            }
            
        })

        return self.users


    