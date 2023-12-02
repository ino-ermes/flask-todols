from flask import jsonify
from http import HTTPStatus

def default_http_handler(e):    
    if not e.message:
        e.message = 'Something went wrong'
    if not e.status_code:
        e.status_code: HTTPStatus.INTERNAL_SERVER_ERROR
    return jsonify(
        message=e.message
    ), e.status_code