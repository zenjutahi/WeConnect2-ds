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
    """ This is a class that gives artributes such as id, name, description and location
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
        """ to get all my businesses """
        return Business.businesslist


class Review(object):
    """ This is a class that gives artributes to a review """
    review_id = 0
    reviewlist = {}

    def __init__(self, business_id, value, comments):
        """ constructor to initialize class """
        Review.review_id += 1 
        self.value = value
        self.comments = comments
        self.business_id = business_id

    def create_Review(self):
        """ To create and store a review """
        self.reviewlist.update({
            self.review_id: {
                'user_id': User.user_id,                
                'business_id': self.business_id,
                'value': self.value,
                'comments': self.comments
                }
        })

        return self.reviewlist

    # def get_Review(self, business_id):
    #     """ To get review for a business"""
    #     reviews = self.reviewlist.items()
    #     one_review = {ke:val for ke, val in reviews if val['business_id'] == business_id}
    #     all_reviews.append(one_review)
    #     return all_reviews



    