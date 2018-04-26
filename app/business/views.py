from flask import flash, request, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash


from flask_jwt_extended import jwt_required, get_jwt_identity

import datetime
import uuid
import json
from functools import wraps
from . import business
from ..app_helper import validate_buss_data_null, check_json, check_blank_key
from ..models import User, Business, Review


@business.route('/businesses', methods=['GET', 'POST'])
@jwt_required
def registerBusiness():
    """ This is to register a business"""
    current_user = get_jwt_identity()
    if request.method == 'POST':
        # Check for json
        if not check_json():
            return jsonify(
                {'message':'Bad Request. Request should be JSON format'}), 405
        # Check for blank key
        try:
            required_fields = ['name', 'description', 'location']
            data = check_blank_key(request.get_json(), required_fields)
        except AssertionError as err:
            msg = err.args[0]
            return jsonify({"message": msg})
        # Check if user entered a name and location
        name = validate_buss_data_null(data['name'])
        description = validate_buss_data_null(data['description'])
        location = validate_buss_data_null(data['location'])
        if not location or not description or not name:
            return jsonify(
                {'message': 'You need a business name and location to Register'}), 403
        # Check if business is registered
        business_dict = Business.businesslist.items()
        existing_business = {
            ke: val for ke,
            val in business_dict if data['name'].lower() == val.name.lower()}
        if existing_business:
            return jsonify(
                {'message': 'This Business is already registered'}), 409
        # If business not registered create one
        new_biz = Business(
            name=data['name'],
            description=data['description'],
            location=data['location'],
            user_id=current_user)
        Business.create_business(new_biz)
        # Get the last businesss registred
        current_business_id = ((sorted(Business.businesslist.keys()))[-1])
        businessName = (Business.businesslist[current_business_id]).name

        return jsonify(
            {'message': 'New business has been created',
             'businesses ID': current_business_id,
             'business name': businessName,
             'user': current_user
             }), 201

        # return jsonify(
        #     {'message': 'You need to log in to register a business'}), 404


    # Get all businesses
    all_businesses = Business.get_businesses_all()
    return jsonify({'message1': 'These are all the businesses',
                    'message': all_businesses
                    }), 200


@business.route('/businesses/<int:business_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required
def editBusiness(business_id):
    current_user = get_jwt_identity()
    business_dict = Business.businesslist
    # Check if business exists
    if not business_dict.get(business_id):
        return jsonify({'message': 'Bussniess does not exist'}), 404
    target_business = business_dict[business_id]
    if current_user != target_business.user_id:
        return jsonify({'message': 'You can only change your own business'}), 403
    # If method is delete, delete the business
    if request.method == 'DELETE':
        del business_dict[business_id]
        return jsonify(
            {'message': 'Business successfully deleted'}), 202
    elif request.method == 'PUT':
        # Check for json
        if not check_json():
            return jsonify(
                {'message':'Bad Request. Request should be JSON format'}), 405
        # Check for blank key
        try:
            required_fields = ['name', 'description', 'location']
            data = check_blank_key(request.get_json(), required_fields)
        except AssertionError as err:
            msg = err.args[0]
            return jsonify({"message": msg})
        # Check for null user data
        name = validate_buss_data_null(data['name'])
        description = validate_buss_data_null(data['description'])
        location = validate_buss_data_null(data['location'])
        if not name or not description or not location:
            return jsonify(
                {'message': 'Business name and Location have to be entred'}), 403

        business_items = Business.businesslist.items()
        existing_business_name = {
            ke: val for ke,
            val in business_items if data['name'] == val.name}
        if existing_business_name:
            return jsonify(
                {'message': 'This Business is already registered'}), 409

        target_business.update_business(data)
        info = {"name": target_business.name,
                "location": target_business.location,
                "description": target_business.description }
        return jsonify({'New business': info ,
                        'message': 'Business edited successfully'
                        }), 201

    info = {"name": target_business.name,
            "location": target_business.location,
            "description": target_business.description }

    return jsonify({'business': info,
                    'message': 'Here is the searched business'
                    }), 200
