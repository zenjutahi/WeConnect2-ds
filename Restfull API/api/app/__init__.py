from flask import Flask, Markup
#local imports
from config import app_config
# Initialize the app

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    from app import models

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api/auth')

    from .business import business as business_blueprint
    app.register_blueprint(business_blueprint, url_prefix='/api' )

    return app



