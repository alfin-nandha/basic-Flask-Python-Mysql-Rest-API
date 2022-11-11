import jwt
import time

from functools import wraps 
from flask import request
from utils import response

from config import config

def generate_JWT(email, id):
    return jwt.encode({
        'email':email, 
        'id':id, 
        'age':(round(time.time())+86400
        )}, config.SECRET_KEY).decode('utf-8')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        try:
            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split('Bearer ')[1]
            
            timestamp = jwt.decode(token, config.SECRET_KEY, algorithms='HS256')['age']
            if not token or timestamp - round(time.time())<0:
                return response.invalid_or_expire_token()
            else :
                return f(*args, **kwargs)

        except jwt.exceptions.DecodeError as Err:
            print(Err)
            if 'Invalid token type' in str(Err):
                return response.invalid_or_expire_token()
            else:
                return response.internal_service_error()

    return decorated

def extract_token():
    token = None
    try:
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split('Bearer ')[1]
            
            if not token:
                return response.invalid_or_expire_token()
        return jwt.decode(token, config.SECRET_KEY, algorithms='HS256')
    
    except jwt.exceptions.DecodeError as Err:
        print(Err)
        if 'Invalid token type' in str(Err):
            return response.invalid_or_expire_token()
        else:
            return response.internal_service_error()
