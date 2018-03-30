'''
Description - Security model
@author - John Sentz
@date - 16-Mar-2018
@time - 6:53 PM
'''
from werkzeug.security import safe_str_cmp

from app.auth.models import User


def authenticate(email, password):
    user = User.find_by_username(email)
    if user and safe_str_cmp(user.password, password):  # use safe string compare from Flask
        return user


def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)
