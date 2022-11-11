from utils import third_party, response
from flask import request

def get_all_book():
    return third_party.get_all_data()

def post_book(data):
    try:
        title = data['title']
        author = data['author']

        if title == None or author == None:
            return response.fail_bad_request()
        print("masukkk")
        resp = third_party.post_data(data)
        print("lagiii")
        return resp

    except Exception as Err:
        print(Err)
        if 'title' in str(Err) or 'name' in str(Err):
            return response.fail_bad_request()
        return response.internal_service_error()