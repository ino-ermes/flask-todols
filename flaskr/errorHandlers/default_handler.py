from flask import jsonify
from http import HTTPStatus

def default_handler(e):
    return (
        jsonify(
            message=str(e),
        ),
        HTTPStatus.INTERNAL_SERVER_ERROR,
    )
    
