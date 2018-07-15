'''
Description - Scheduler Model
@author - John Sentz
@date - 02-Jul-2018
@time - 6:08 PM
'''

import requests

from app import db


class Schedule(db.Model):
    __tablename__ = 'schedule'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(512))
    start_date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_date = db.Column(db.Date)
    end_time = db.Column(db.Time)
    default = db.Column(db.Boolean, default=False)
    continuous = db.Column(db.Boolean, default=False)


