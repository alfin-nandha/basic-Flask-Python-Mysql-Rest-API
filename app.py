import os
import usecase.user as user_case

from flask import Flask, request
from config import config
from utils.token import token_required

# string router url const 
REGISTER = '/register'
USERS = '/users'
USER_BY_ID = '/users/<id>'
LOGIN = '/login'

# flask app
app = Flask(__name__)
app.config.from_pyfile(os.path.abspath(config.__file__))



@app.route(REGISTER, methods = ['POST'])
def resgister():
    return user_case.insert_user(request.get_json())

@app.route(USERS, methods=['GET'])
def users():
    return user_case.get_all_users()

@app.route(USER_BY_ID, methods=['GET', 'PUT', 'DELETE'])
@token_required
def user(id):
    if request.method == 'GET':
        return user_case.get_user_by_id(id)
    elif request.method == 'DELETE':
        return user_case.delete_user_by_id(id)
    elif request.method == 'PUT':
        return user_case.update_user_by_id(request.get_json(), id)

@app.route(LOGIN, methods=['POST'])
def login():
    return user_case.login(request.get_json())


if __name__ == '__main__':
    app.run()
