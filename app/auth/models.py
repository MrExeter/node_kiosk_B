'''
Description - User Model
@author - John Sentz
@date - 09-Mar-2018
@time - 1:10 PM
'''

from datetime import datetime
from app import db, bcrypt
from flask_login import UserMixin
from app import login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(48))
    user_email = db.Column(db.String(60), unique=True, index=True)
    user_password = db.Column(db.String(128))
    registration_date = db.Column(db.DateTime, default=datetime.now)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.user_password, password)

    @classmethod
    def create_user(cls, user, email, password):
        user = cls(user_name=user,
                   user_email=email,
                   user_password=bcrypt.generate_password_hash(password).decode('utf-8'))

        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(user_email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

