from flask import flash, request, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash


import jwt
import datetime
import uuid
import json
from functools import wraps
from . import review
from ..models import User, Business, Review

@review.route('/<int:buzId>/reviews', methods=['GET', 'POST'])
def make_businessreview(buzId):
    if request.method == 'POST':

        data = request.get_json()

        business_dict = Business.businesslist
        businessIds = business_dict.keys()
        if buzId not in businessIds: 
            return jsonify({'message':'You can only review an existing business'}), 409
        
        new_review = Review(business_id=buzId, value=data['value'], comments=data['comments'])
        new_review.create_Review()

        return jsonify({'message':'You have successfully created a review',
                        'message2': Review.reviewlist }), 201
    #retreving a single business's reviews
    reviews = Review.reviewlist.items()
    business_review = {ke:val for ke, val in reviews if val['business_id'] == buzId }
    return jsonify({'message': 'Business reviews succesfully retreaved',
                    'Reviews are:': business_review.key()['value']}), 201




