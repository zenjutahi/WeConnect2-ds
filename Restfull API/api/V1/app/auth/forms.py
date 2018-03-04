from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextField
from wtforms.validators import DataRequired, Length, Email


class RegistrationForm(FlaskForm):
    """ To render and validate the signup form"""

    email = StringField("Email", validators=[DataRequired(),
                        Email(), Length(max=32)])
    username = StringField("Username", validators=[DataRequired(),
                        Length(4, 32)])
    password = StringField("Password", validators=[DataRequired(),
                        Length(min=6, max=32)])