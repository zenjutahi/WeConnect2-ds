from flask import flash, request, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash


import jwt
import datetime
import uuid
import json
from functools import wraps
from . import business
from ..models import User, Business, Review

global logged_in
logged_in = False




@business.route('/businesses', methods=['GET','POST'])
def registerBusiness():
    """ This is to register a business"""
    if request.method == 'POST':

        data = request.get_json()
        if True:
            #check if user entered a name and location 
            if data['name'] == "" or data['location'] == "":
                return jsonify({'message': 'You need a business name and location to Register'}), 403

            business_dict = Business.businesslist.items()
            existing_business = {ke:val for ke, val in  business_dict if data['name'] in val['name']}
            if existing_business:
                return jsonify({'message':'This Business is already registered'}), 409

            #If business not registered create one

            new_biz = Business(name=data['name'], description=data['description'], location=data['location'])
            new_biz.create_business()
            #get the last businesss
            current_business_id = ((sorted(Business.businesslist.keys()))[-1])
            businessName = Business.businesslist[current_business_id]['name']

            return jsonify(
                {'message':'New business has been created',
                'businesses ID': current_business_id,
                'business name': businessName
                }), 201

        return jsonify({'message':'You need to log in to register a business'}), 404

    #This get all businesses 
    all_businesses = Business.get_businesses_all()
    return jsonify({ 'message1': 'These are all the businesses',
                     'message': all_businesses
                     }), 200


@business.route('/businesses/<int:buzId>', methods=['GET', 'PUT', 'DELETE'])
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
    elif request.method == 'PUT':
        for businessId in businessIds:
            if businessId == buzId:
                data = request.get_json()
                targetBusinessValues = business_dict[buzId]
                if data['name'] == "" or data['location'] == "":
                    return jsonify({'message': 'Business name and Location have to be entred'}), 403
                for values in targetBusinessValues:
                    targetBusinessValues['name'] = data['name']
                    targetBusinessValues['description'] = data['description']
                    targetBusinessValues['location'] = data['location']
                    return jsonify({'New business': targetBusinessValues,
                                    'message': 'Business Edited successfully'
                                    }), 201

    else:
        for businessId in businessIds:
            if businessId == buzId:
                targetBusiness = business_dict[buzId]
                return jsonify({'business': targetBusiness,
                                'business Id': buzId,
                                'message': 'Here is the searched business'
                                
                                }), 200
    