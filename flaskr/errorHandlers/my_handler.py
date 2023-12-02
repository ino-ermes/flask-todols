from flask import jsonify
from http import HTTPStatus
from flaskr.errors.custom_api import CustomAPIError

def my_handler(e):    
    return jsonify(e.to_dict()), e.status_code
