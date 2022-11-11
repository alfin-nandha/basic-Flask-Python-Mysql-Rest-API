import requests
from utils.const import THIRD_URL
from utils import response
from config import config

host = config.THIRD_HOST

def get_all_data():
    url = (host + THIRD_URL.BOOKS)
    data = requests.get(url).json()
    
    if data == None:
        return response.fail_data_not_found()
    return response.success_get_data(data)

def post_data(data):
    url = (host + THIRD_URL.BOOKS)
    resp = requests.post(url,data).json()
    if resp['id'] == 0:
        return response.fail_bad_request()
    return response.success_create()