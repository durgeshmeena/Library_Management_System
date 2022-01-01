from flask import flash, session, redirect, url_for
from functools import wraps
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField
from wtforms.validators import Email
import re


class LoginForm(FlaskForm):
    email = StringField('Email', [Email("Email is not valid.")])
    password = PasswordField("Password")
    checkbox = BooleanField(default="checked")

    def validate(self, extra_validators=None):
        if super().validate(extra_validators):
           
            if not self.password.data:
                self.password.errors.append('Password is required.')
                return False
            elif len(self.password.data)<6:
                self.password.errors.append('Password length must be greater than 5 charactars')
                return False    
            else:
                return True    
        return False

#  Signup form 
class SignupForm(FlaskForm):
    name = StringField('Name')
    email = StringField('Email', [Email("Email is not valid!!")])
    username = StringField('Username') 
    password = PasswordField("Password")

    def validate(self, extra_validators=None):
        if super().validate(extra_validators):
            
            if not self.username.data:
                self.username.errors.append('Username is required.')
                return False
            elif not bool(re.match("^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$",self.username.data)):
                self.username.errors.append('Username is not valid.')
                return False


            elif not self.password.data:
                self.password.errors.append('Password is required.')
                return False
            elif len(self.password.data)<6:
                self.password.errors.append('Password length must be greater than 5 charactars')
                return False    
            else:
                return True    
        return False


def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{error}', 'danger')


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first", 'danger')
            return redirect(url_for('login'))
    return wrap