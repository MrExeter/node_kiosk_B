'''
Description - Production run configuration
@author - John Sentz
@date - 20-Nov-2018
@time - 11:19 AM
'''

DEBUG = False
SECRET_KEY = 'ZvseANqiPDdeXuPJa4QedKAbjh2XYoLY'
WTF_CSRF_SECRET_KEY = 'ZvseANqiPDdeXuPJa4QedKAbjh2XYoLY'
# SQLALCHEMY_DATABASE_URI = 'postgresql://pi:applejack@localhost/kiosk_db'
SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
SQLALCHEMY_TRACK_MODIFICATIONS = False
