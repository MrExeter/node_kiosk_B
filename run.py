'''
Description - Main app for kiosk controller
@author - John Sentz
@date - 10-Apr-2018
@time - 10:31 AM
'''
from flask import session
from omxplayer.player import OMXPlayer

from app import create_app, db
from app.auth.models import User

if __name__ == '__main__':
    flask_app = create_app('dev')

    # # JWT Authentication
    # api = Api(flask_app)
    # jwt = JWT(flask_app, authenticate, identity)  # generates endpoint /auth

    with flask_app.app_context():
        db.create_all()

        if not User.query.filter_by(user_name='napoleon').first():
            User.create_user(user='napoleon',
                             email='napoleon@dynamite.com',
                             password='applejack')

    flask_app.run(debug=True, host='0.0.0.0', port=5100)

