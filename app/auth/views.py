from flask import flash, request, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash


import jwt
import datetime
import uuid
from functools import wraps
from . import auth
from ..models import User
from app import create_app


# Set var to check user login status
global logged_in
logged_in = False

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
            data = jwt.decode(token, app.config['SECRET_KEY'])
            users_dict = User.users.items()
            current_user = {
                ke: val for ke,
                val in users_dict if data['email'] in val['email']}
        except BaseException:
            return jsonify({'message': 'Token is invalid!'}), 401
        return func(current_user, *args, **kwargs)

    return decorated


@auth.route('/register', methods=['GET', 'POST'])
def register():
    data = request.get_json()

    if data['email'] == "" or data["password"] == "":
        return jsonify(
            {'message': 'You need email and password to login'}), 401

    # check if email already registred
    users_dict = User.users.items()
    existing_user = {
        ke: val for ke,
        val in users_dict if data['email'] in val['email']}
    if existing_user:
        print(existing_user)
        return jsonify(
            {'message': 'This email is registered, login instead'}), 404

    # If email not registred, create user account
    new_user = User(
        email=data['email'],
        username=data['username'],
        password=data['password'])
    new_user.create_user()

    # give user session
    for key, value in users_dict:
        if data['email'] in value['email']:
            session['user_id'] = key

    return jsonify({'message': 'New user Succesfully created'}), 201


# user_id=str(uuid.uuid4()),

@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.get_json()
    if data['email'] == "" or data["password"] == "":
        return jsonify(
            {'message': 'You need both password and username to login'}), 401

    users_dict = User.users.items()
    existing_user = {
        ke: val for ke,
        val in users_dict if data['email'] in val['email']}
    if existing_user:
        valid_user = [
            va for va in existing_user.values() if check_password_hash(
                va['password'], data['password'])]
        if valid_user:
            global logged_in
            logged_in = True

            # Give user session
            for key, value in users_dict:
                if data['email'] in value['email']:
                    session['user_id'] = key

            token = jwt.encode({'email': data['email'], 'exp': datetime.datetime.utcnow(
            ) + datetime.timedelta(minutes=15)}, app.config['SECRET_KEY'])
            return jsonify({'message': 'User valid and succesfully logged in',
                            'token': token.decode('UTF-8')}), 200

        else:
            return jsonify({'message': 'Wrong password'}), 403

    else:
        return jsonify({'message': 'Not registered user'}), 400


@auth.route('/logout')
@token_required  # current_user --- to be passed when using token
def logout(current_user):
    global logged_in
    logged_in = False

    session.pop('user_id', None)

    return jsonify({'message': 'Succesfully logged out'}), 200


@auth.route('/reset-password')
def reset_password():
    pass
