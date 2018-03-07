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


class Business(object):
    """ This is a class that gives artributes such as id, name, description 
              to a business """

    buss_id = 0
    businesslist = {}

    def __init__(self, name, description, location):
        """ constructor to initialize class """

        Business.buss_id += 1 
        self.name = name
        self.description = description
        self.location = location 

    def create_business(self):
        """ To create and store a business """
        self.businesslist.update({
            self.buss_id: {
                'user_id':User.user_id,
                'name': self.name,
                'description': self.description,
                'location': self.location
                }
        })

        return self.businesslist
        
    @staticmethod
    def get_businesses_all():
        """ to get all my business """
        return Business.businesslist


    