import os

FLASK_DEBUG = os.getenv('FLASK_DEBUG')

DB_HOST = os.getenv('DB_HOST_DEV') if FLASK_DEBUG == '1' else os.getenv('DB_HOST')
DB_DATABASE = os.getenv('DB_NAME_DEV') if FLASK_DEBUG == '1' else os.getenv('DB_NAME')
DB_USERNAME = os.getenv('DB_USERNAME_DEV') if FLASK_DEBUG == '1' else os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWROD_DEV') if FLASK_DEBUG == '1' else os.getenv('DB_PASSWORD')

SECRET_KEY = 'my_secret'