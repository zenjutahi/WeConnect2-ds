from flask import flash, request, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash


from flask_jwt_extended import jwt_required

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
    if request.method == 'POST':
        if check_json():
            try:
                required_fields = ['name', 'description', 'location']
                data = check_blank_key(request.get_json(), required_fields)
            except AssertionError as err:
                msg = err.args[0]
                return jsonify({"message": msg})
            name = validate_buss_data_null(data['name'])
            description = validate_buss_data_null(data['description'])
            location = validate_buss_data_null(data['location'])
            if True:
                # check if user entered a name and location
                if not location or not description or not name:
                    return jsonify(
                        {'message': 'You need a business name and location to Register'}), 403

                business_dict = Business.businesslist.items()
                existing_business = {
                    ke: val for ke,
                    val in business_dict if data['name'] == val.name}
                if existing_business:
                    return jsonify(
                        {'message': 'This Business is already registered'}), 409
                # If business not registered create one

                new_biz = Business(
                    name=data['name'],
                    description=data['description'],
                    location=data['location'])
                Business.create_business(new_biz)
                # get the last businesss
                current_business_id = ((sorted(Business.businesslist.keys()))[-1])
                businessName = (Business.businesslist[current_business_id]).name

                return jsonify(
                    {'message': 'New business has been created',
                     'businesses ID': current_business_id,
                     'business name': businessName
                     }), 201

            return jsonify(
                {'message': 'You need to log in to register a business'}), 404

        return jsonify(
            {'message':'Bad Request. Request should be JSON format'}), 405

    # This get all businesses
    all_businesses = Business.get_businesses_all()
    return jsonify({'message1': 'These are all the businesses',
                    'message': all_businesses
                    }), 200


@business.route('/businesses/<int:business_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required
def editBusiness(business_id):

    business_dict = Business.businesslist
    if business_dict.get(business_id):
        target_business = business_dict[business_id]
        if request.method == 'DELETE':
            del business_dict[business_id]
            return jsonify(
                {'message': 'Business successfully deleted'}), 202
        elif request.method == 'PUT':
            if check_json():
                try:
                    required_fields = ['name', 'description', 'location']
                    data = check_blank_key(request.get_json(), required_fields)
                except AssertionError as err:
                    msg = err.args[0]
                    return jsonify({"message": msg})
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
                                'message': 'Business Edited successfully'
                                }), 201
            return jsonify(
                {'message':'Bad Request. Request should be JSON format'}), 405

        info = {"name": target_business.name,
                "location": target_business.location,
                "description": target_business.description }

        return jsonify({'business': info,
                        'message': 'Here is the searched business'

                        }), 200

    return jsonify({'message': 'Bussniess Id unknown'}), 404
