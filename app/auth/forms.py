'''
Description - User authorization forms
@author - John Sentz
@date - 09-Mar-2018
@time - 5:39 PM
'''


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from app.auth.models import User


def email_exists(form, field):
    # Check to see if email is already in database
    email = User.query.filter_by(user_email=field.data).first()
    if email:
        raise ValidationError('Email Already Exists')


class RegistrationForm(FlaskForm):

    name = StringField('Whats your Name', validators=[DataRequired(),
                                                      Length(3, 20, message='between 3 to 20 characters')])

    email = StringField('Enter your Email', validators=[DataRequired(),
                                                        Email(),
                                                        email_exists])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(8),
                                                     EqualTo('confirm', message='passwords must match')])
    confirm = PasswordField('Confirm', validators=[DataRequired()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    class Meta:
        csrf = False

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    stay_loggedin = BooleanField('stay logged-in')
    submit = SubmitField('Login')

