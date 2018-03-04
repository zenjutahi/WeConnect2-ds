from flask import flash, redirect, render_template, url_for, request, session, Markup

from . import auth
from .forms import RegistrationForm
from ..models import User


# Set var to check user login status
global logged_in
logged_in = False

@auth.route('/register', methods=['GET', 'POST'])
def register():
    global logged_in
    if logged_in:
        return logout_required()
    else:
        form = RegistrationForm(request.form)

        if form.validate_on_submit():
            # Return error if email is registred

            users_dict = User.users.items()
            existing_user = {k:v for k, v in users_dict if form.email.data in v['email']}
            if existing_user:
                email_exists = Markup("<div class='alert alert-info' role='alert'>\
                                            The email entered is registered, please login instead\
                                        </div>")
                flash(email_exists)

                return render_template()

            # Register user if email not registered
            new_user = User(form.email.data, form.username.data, form.password.data)
            new_user.create_user()

            for key, value in users_dict:
                if form.email.data in value['email']:
                    session['user_id'] = key

            successful_signup = Markup("<div class='alert alert-success' role='alert'>\
                                            Account created successfully\
                                        </div>")

            flash(successful_signup)

            return redirect(url_for())

        if form.errors:
            if len(form.password.data) < 4:
                form_error = Markup("<div class='alert alert-danger' role='alert'>\
                                        Password should be more than 4 chars\
                                    </div>")
                flash(form_error)
            if len(form.username.data) < 4:
                form_error = Markup("<div class='alert alert-danger' role='alert'>\
                                        Username should be more than 4 chars\
                                    </div>")
                flash(form_error)
            else:
                form_error = Markup("<div class='alert alert-danger' role='alert'>\
                                        Enter valid email, like j.deere@mail.com\
                                    </div>")
                flash(form_error)

    logged_in = False # for GET method
    return render_template(form=form)
        