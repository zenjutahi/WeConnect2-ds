from flask import Flask, Markup
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
#local imports
from config import app_config
# Initialize the app

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    from app import models
    from app.auth.views import resettoken_store

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api/auth')

    from .business import business as business_blueprint
    app.register_blueprint(business_blueprint, url_prefix='/api' )

    from .review import review as review_blueprint
    app.register_blueprint(review_blueprint, url_prefix='/api/businesses' )

    # @jwt.token_in_blacklist_loader
    # def check_if_token_in_reset_store():
    #     jti = decrypted_token['jti']
    #     return jti in resettoken_store

    
    jwt = JWTManager(app)
    return app
