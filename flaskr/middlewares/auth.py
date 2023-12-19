from functools import wraps
import jwt
from flask import request
import bson, os
from flaskr.errors.unauthenicated import UnauthenticatedError
from flaskr.models.User import _userColl


def access_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            try:
                token = request.headers["Authorization"].split(" ")[1]
            except:
                raise UnauthenticatedError("Invalid Authentication Header!")
        if not token:
            raise UnauthenticatedError("Authentication Token is missing!")

        data = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
        
        userId = data["user_id"]

        if userId is None:
            raise UnauthenticatedError("Invalid Authentication token!")

        return f(userId, *args, **kwargs)

    return decorated
