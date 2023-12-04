from flask import jsonify
from http import HTTPStatus
from werkzeug.exceptions import HTTPException

def default_http_handler(e):
    message = 'Url does not exist'
    status_code = HTTPStatus.NOT_FOUND
    
    if isinstance(e, HTTPException):
        message = e.description or 'Url does not exist'
        status_code = e.response.status_code if e.response else HTTPStatus.NOT_FOUND

    return jsonify(
        message=message
    ), status_code
        