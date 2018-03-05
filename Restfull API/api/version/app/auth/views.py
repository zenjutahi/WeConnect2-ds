from flask import flash, url_for, request, session, Markup, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

import uuid
from . import auth
from ..models import User


# Set var to check user login status
global logged_in
logged_in = False

@auth.route('/register', methods=['GET', 'POST'])
def register():
    data = request.get_json()
    # Check if email already registred
    users_dict = User.users.items()
    existing_user = {k:v for k, v in users_dict if data['email'] in v['email']}
    if existing_user:
        return jsonify({'message':'This email is registered, login instead'})


    # If email not registred, create user account
    new_user = User(email=data['email'], username=data['username'], password=data['password'])
    new_user.create_user()

    for key, value in users_dict:     # user gets id, eg 3
        if data['email'] in value['email']:
            session['user_id'] = key

    return jsonify({'message' : 'New user Succesfully created'})


#user_id=str(uuid.uuid4()),

@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.get_json()

    users_dict = User.users.items()
    existing_user = {k:v for k, v in users_dict if data['email'] in v['email']}
    if existing_user:
        valid_user = [v for v in existing_user.values() if check_password_hash(v
                        ['password'], data['password'])]
        if valid_user:
            global logged_in
            logged_in = True

            for key, value in users_dict:     # user gets id, eg 3
                if data['email'] in value['email']:
                    session['user_id'] = key
            return jsonify({'message' : 'User valid succesfully logged in'})

        else:
            return jsonify({'mesage': 'Wrong password'})

    else:
        return jsonify({'message': 'Not registered user'})

@auth.route('/logout')
def logout():
    global logged_in
    logged_in = False

    session.pop('user_id', None)

    return jsonify({'message' : 'Succesfully logged out'})