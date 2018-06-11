from flask import flash, request, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash


from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime
import uuid
import json
from functools import wraps
from . import review
from ..app_helper import validate_buss_data_null, check_json, check_blank_key
from ..models import User, Business, Review


@review.route('/<int:business_id>/reviews', methods=['GET', 'POST'])
@jwt_required
def make_businessreview(business_id):
    current_user = get_jwt_identity()
    business_dict = Business.businesslist
    businessIds = business_dict.keys()
    if request.method == 'POST':
        if check_json():
            try:
                required_fields = ['value', 'comments']
                data = check_blank_key(request.get_json(), required_fields)
            except AssertionError as err:
                msg = err.args[0]
                return jsonify({"message": msg})
            value = validate_buss_data_null(data['value'])
            comments = validate_buss_data_null(data['comments'])

            if business_id not in businessIds or len(businessIds) == 0:
                return jsonify(
                    {'message': 'You can only review an existing business'}), 409
            target_business = business_dict[business_id]
            if current_user == target_business.user_id:
                return jsonify({'message': 'You can not review your own business'}), 403
            if not value or not comments:
                return jsonify(
                    {'message': 'You have to enter a review value and comment'}), 400
            new_review = Review(
                business_id = business_id,
                value=data['value'],
                comments=data['comments'])
            Review.create_Review(new_review)
            current_review_id = ((sorted(Review.reviewlist.keys()))[-1])
            review_value = (Review.reviewlist[current_review_id]).value
            review_comment = (Review.reviewlist[current_review_id]).comments


            return jsonify({'message': 'You have successfully created a review',
                            'Value': review_value,
                            'Comments': review_comment}), 201

        return jsonify(
            {'message':'Bad Request. Request should be JSON format'}), 405

    # retreving a single business's reviews
    if business_id not in businessIds or len(businessIds) == 0:
        return jsonify({'message': 'Enter a registred business'}), 409

    reviews = Review.reviewlist.values()
    target_reviews = []
    for review in reviews:
        if review.business_id == business_id:
            target_reviews.append(review)

    reviews_info = []
    for review in target_reviews:
        info = {"Id": review.id,
        "value": review.value,
        "comments": review.comments}
        reviews_info.append(info)


    return jsonify({'message': 'Business reviews succesfully retreaved',
                    'Reviews are:': reviews_info}), 201
