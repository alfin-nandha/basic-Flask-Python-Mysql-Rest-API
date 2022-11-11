from flask import request
from app import app

from usecase import user as user_case
from usecase import book as book_case
from utils.token import token_required
from utils.const import URL

@app.route(URL.REGISTER, methods = ['POST'])
def resgister():
    return user_case.insert_user(request.get_json())

@app.route(URL.USERS, methods=['GET'])
def users():
    return user_case.get_all_users()

@app.route(URL.USER_BY_ID, methods=['GET', 'PUT', 'DELETE'])
@token_required
def user(id):
    if request.method == 'GET':
        return user_case.get_user_by_id(id)
    elif request.method == 'DELETE':
        return user_case.delete_user_by_id(id)
    elif request.method == 'PUT':
        return user_case.update_user_by_id(request.get_json(), id)

@app.route(URL.LOGIN, methods=['POST'])
def login():
    return user_case.login(request.get_json())

@app.route(URL.BOOKS, methods=['GET', 'POST'])
def books():
    if request.method == 'GET':
        return book_case.get_all_book()
    elif request.method == 'POST':
        return book_case.post_book(request.get_json())