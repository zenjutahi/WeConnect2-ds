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
    data = request.get_json()

    business_dict = Business.businesslist
    businessIds = business_dict.keys()
    if request.method == 'POST':


        if buzId not in businessIds or len(businessIds) == 0: 
            return jsonify({'message':'You can only review an existing business'}), 409
        if data['value'] == "":
            return jsonify({'message': 'You have to enter a review value'}), 400
        new_review = Review(business_id=buzId, value=data['value'], comments=data['comments'])
        new_review.create_Review()

        return jsonify({'message':'You have successfully created a review',
                        'message2': Review.reviewlist }), 201

    #retreving a single business's reviews
    if buzId not in businessIds or len(businessIds) == 0:
        return jsonify({'message':'Enter a registred business'}), 409
    reviews = Review.reviewlist.items()
    business_review = {ke:val for ke, val in reviews if val['business_id'] == buzId }
    return jsonify({'message': 'Business reviews succesfully retreaved',
                    'Reviews are:': business_review}), 201




