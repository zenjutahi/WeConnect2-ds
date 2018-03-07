from flask import flash, request, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash


import jwt
import datetime
import uuid
import json
from functools import wraps
from . import busz
from ..models import User, Business


@busz.route('/businesses', methods=['GET','POST'])
def register_biz():
    """ This is to register a business"""
    if request.method == 'POST':

        data = request.get_json()

        #check if user entered a name 
        if data['name'] == "" :
            return jsonify({'message': 'You need a business name to Register'}), 403

        business_dict = Business.businesslist.items()
        existing_business = {ke:val for ke, val in  business_dict if data['name'] in val['name']}
        if existing_business:
            return jsonify({'message':'This Business is already registered'}), 404

        #If business not registered create one

        new_biz = Business(name=data['name'], description=data['description'], location=data['location'])
        new_biz.create_business()
        """ get the last businesss """
        current_biz_id = ((sorted(Business.businesslist.keys()))[-1])
        biz = Business.businesslist[current_biz_id]['name']

        return jsonify(
            {'message':'New business has been created',
            'businesses': current_biz_id,
            'biz': biz
            }), 201

    """ This is to get all businesses """
    all_businesses = Business.get_businesses_all()
    return jsonify(all_businesses)


@busz.route('/businesses/<int:buzId>', methods=['GET', 'POST', 'DELETE'])
def editBusiness(buzId):

    business_dict = Business.businesslist
    businessIds = business_dict.keys()
    if buzId not in businessIds:
        return jsonify({'message':'Bussniess Id unknown'}), 404
    if request.method == 'DELETE':
        for businessId in businessIds:
            if businessId == buzId:
                del business_dict[buzId]
                return jsonify({'message': 'Business successfully deleted'}), 202