'''
Description - Development run configuration
@author - John Sentz
@date - 20-Nov-2018
@time - 11:18 AM
'''

DEBUG = True
SECRET_KEY = 'applejack'
WTF_CSRF_SECRET_KEY = 'applejack'
# SQLALCHEMY_DATABASE_URI = 'postgresql://pi:applejack@localhost/kiosk_db'
SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
SQLALCHEMY_TRACK_MODIFICATIONS = False
