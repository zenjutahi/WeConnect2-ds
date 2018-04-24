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
        self.id = User.user_id
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)
    @classmethod
    def create_user(cls, new_user):
        """ Class to create and store a user object """
        cls.users.update({
            new_user.id: new_user
        })

        return cls.users

    def update_user(self, data):
        """ Updates a business """
        valid_fields = ['password']
        for field in data:
            if field in valid_fields:
                new_data = generate_password_hash(data[field])
                setattr(self, field, new_data)


class Business(object):
    """ This is a class that gives artributes such as id, name, description and location
                            to a business """

    buss_id = 0
    businesslist = {}

    def __init__(self, name, description, location, user_id):
        """ constructor to initialize class """

        Business.buss_id += 1
        self.id = Business.buss_id
        self.name = name
        self.description = description
        self.location = location
        self.user_id = user_id

    @classmethod
    def create_business(cls, business):
        """ To create and store a business """
        cls.businesslist.update({
            business.id: business
        })


        return cls.businesslist

    def update_business(self, data):
        """ Updates a business """
        valid_fields = ['name', 'description', 'location']
        for field in data:
            if field in valid_fields:
                setattr(self, field, data[field])



    @staticmethod
    def get_businesses_all():
        """ to get all my businesses """
        businesses = []
        fields = ['id', 'name', 'description', 'location']
        for business in Business.businesslist.values():
            business_info = {}
            for field in fields:
                business_info[field] = getattr(business, field)
            businesses.append(business_info)
        return businesses


class Review(object):
    """ This is a class that gives artributes to a review """
    review_id = 0
    reviewlist = {}

    def __init__(self, business_id, value, comments):
        """ constructor to initialize class """
        Review.review_id += 1
        self.id = Review.review_id
        self.value = value
        self.comments = comments
        self.business_id = business_id

    @classmethod
    def create_Review(cls, review):
        """ To create and store a review """
        cls.reviewlist.update({
            review.id : review
        })

        return cls.reviewlist
