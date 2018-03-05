from flask import flash, url_for, request, session, Markup, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

import uuid
from . import auth
from ..models import User


# Set var to check user login status

@auth.route('/register', methods=['GET', 'POST'])
def register():
    data = request.get_json()

    new_user = User(email=data['email'], username=data['username'], password=data['password'])
    new_user.create_user()

    return jsonify({'message' : 'New user created'})

    
#user_id=str(uuid.uuid4()),