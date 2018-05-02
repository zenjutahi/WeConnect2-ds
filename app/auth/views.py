from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
        JWTManager, jwt_required, create_access_token,
        get_jwt_identity, get_raw_jwt
        )
import datetime
# import uuid
# from functools import wraps
from . import auth
from ..models import User
from ..app_helper import validate_auth_data_null, check_json, validate_email,check_blank_key
from app import create_app

resettoken_store = set()
blacklist = set()


@auth.route('/register', methods=['POST'])
def register():
    # Check for json
    if not check_json():
        return jsonify(
                {'message':'Bad Request. Request should be JSON format'}), 405

    # Check for blank key
    try:
        required_fields = ['email', 'password', 'username']
        data = check_blank_key(request.get_json(), required_fields)
    except AssertionError as err:
        msg = err.args[0]
        return jsonify({"message": msg})
    # Check for null in user data
    email = validate_auth_data_null(data['email'])
    password = validate_auth_data_null(data['password'])
    username = validate_auth_data_null(data['username'])
    if not email or not password or not username:
        return jsonify(
            {'message': 'You need email, username and password to register'}), 401
    # Check valid email
    if not validate_email(email):
        return jsonify(
                {'message':'Invalid Email. Enter valid email to register'}), 400
    # Check if email already registred
    users_dict = User.users.items()
    existing_user = {
        ke: val for ke,
        val in users_dict if email.lower() == val.email.lower() }
    if existing_user:
        print(existing_user)
        return jsonify(
            {'message': 'This email is registered, login instead'}), 404

    # If email not registred, create user account
    new_user = User(
        email=data['email'],
        username=data['username'],
        password=data['password'])
    User.create_user(new_user)
    return jsonify({'message': 'New user Succesfully created'}), 201





@auth.route('/login', methods=['POST'])
def login():

    # Check for json
    if not check_json():
        return jsonify(
                {'message':'Bad Request. Request should be JSON format'}), 405
    # Check for blank key
    try:
        required_fields = ['email', 'password']
        data = check_blank_key(request.get_json(), required_fields)
    except AssertionError as err:
        msg = err.args[0]
        return jsonify({"message": msg})
    # Check for null in user data
    email = validate_auth_data_null(data['email'])
    password = validate_auth_data_null(data['password'])
    if not email or not password:
        return jsonify(
            {'message': 'You need both password and username to login'}), 401
    # Ensure user exists
    users_dict = User.users.items()
    existing_user = {
        ke: val for ke,
        val in users_dict if data['email'] == val.email}
    if not existing_user:
        return jsonify({'message': 'Not registered email'}), 400
    # Validate login data
    valid_user = [
        va for va in existing_user.values() if check_password_hash(
            va.password, data['password'])]
    if not valid_user:
        return jsonify({'message': 'Wrong password'}), 403
    # If valid login user
    expires=datetime.timedelta(minutes=10)
    access_token = create_access_token(identity=email,expires_delta=expires)
    return jsonify({'message': 'User valid and succesfully logged in',
                    'token': access_token}), 200



@auth.route('/logout') #, methods=['DELETE']
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({'message': 'Succesfully logged out'}), 200


@auth.route('/reset-password', methods=['POST'])
def reset_password():
    if not check_json():
        return jsonify(
                {'message':'Bad Request. Request should be JSON format'}), 405
    data = request.get_json()
    email = validate_auth_data_null(data['email'])
    if not email:
        return jsonify(
            {'message': 'You need your email to reset password'}), 401
    users_dict = User.users.items()
    existing_user = {
        ke: val for ke,
        val in users_dict if data['email'] == val.email}
    if not existing_user:
        return jsonify({'message': 'Not registered email'}), 400
    pass_reset_token = create_access_token(identity=email)
    resettoken_store.add(pass_reset_token)
    return jsonify(
            {'message': 'Use this token to reset password',
             'reset-token': pass_reset_token}), 200


@auth.route('/reset-password/update', methods=['POST'])
def update_password():
    url_access_token = request.args.get('reset-token')
    if not check_json():
        return jsonify(
                {'message':'Bad Request. Request should be JSON format'}), 405
    data = request.get_json()
    email = validate_auth_data_null(data['email'])
    password = validate_auth_data_null(data['password'])
    if not password:
        return jsonify(
            {'message': 'You need your password'}), 401
    if url_access_token not in resettoken_store:
        return jsonify(
                {'message':'You need the access token to update password'}), 405
    all_users = User.users.values()
    target_user = None
    for user in all_users:
        if user.email == data['email']:
            target_user = user
            break
    if target_user:
        target_user.update_user(data)
        return jsonify(
                {'message':'Password Succesfully changed'}), 201

    return jsonify(
            {'message':'Enter the email you used to reset password'}), 403
