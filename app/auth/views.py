from flask import flash, request, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash


import jwt
import datetime
import uuid
from functools import wraps
from . import auth
from ..models import User
from ..app_helper import validate_auth_data_null, check_json, validate_email
from app import create_app

app = create_app(config_name='development')


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithm=['HS256'])
            users_dict = User.users.items()
            current_user = {
                ke: val for ke,
                val in users_dict if data['email'] in val.email}
        except BaseException:
            return jsonify({'message': 'Token is invalid!'}), 401
        return func(current_user, *args, **kwargs)

    return decorated


@auth.route('/register', methods=['POST'])
def register():
    #check for json
    if check_json():
        data = request.get_json()
        email = validate_auth_data_null(data['email'])
        password = validate_auth_data_null(data['password'])
        username = validate_auth_data_null(data['username'])

        # check for null
        if not email or not password or not username:
            return jsonify(
                {'message': 'You need email and password to login'}), 401
        # check valid email
        if validate_email(email):
            # check if email already registred
            users_dict = User.users.items()
            existing_user = {
                ke: val for ke,
                val in users_dict if email in val.email }
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

        return jsonify(
                {'message':'Invalid Email. Enter valid email to register'}), 400

    return jsonify(
            {'message':'Bad Request. Request should be JSON format'}), 405


@auth.route('/login', methods=['POST'])
def login():

    #check for json
    if check_json():
        data = request.get_json()
        email = validate_auth_data_null(data['email'])
        password = validate_auth_data_null(data['password'])
        if not email or not password:
            return jsonify(
                {'message': 'You need both password and username to login'}), 401

        users_dict = User.users.items()
        existing_user = {
            ke: val for ke,
            val in users_dict if data['email'] in val.email}
        if existing_user:
            valid_user = [
                va for va in existing_user.values() if check_password_hash(
                    va.password, data['password'])]
            if valid_user:
                # generate token for user
                token = jwt.encode({'email': data['email'], 'exp': datetime.datetime.utcnow(
                ) + datetime.timedelta(minutes=15)}, app.config['SECRET_KEY'], algorithm='HS256')
                print(token)
                return jsonify({'message': 'User valid and succesfully logged in',
                                'token': token.decode('UTF-8')}), 200

            else:
                return jsonify({'message': 'Wrong password'}), 403

        else:
            return jsonify({'message': 'Not registered email'}), 400

    return jsonify(
            {'message':'Bad Request. Request should be JSON format'}), 405

@auth.route('/logout')
@token_required
def logout(current_user):

    return jsonify({'message': 'Succesfully logged out'}), 200


@auth.route('/reset-password')
def reset_password():
    pass
