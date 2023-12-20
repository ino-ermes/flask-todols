from functools import wraps
import jwt
from flask import request
import os, bson
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

        requestUserId = data["user_id"]

        if requestUserId is None:
            raise UnauthenticatedError("Invalid Authentication token!")

        return f(requestUserId, *args, **kwargs)

    return decorated


def admin_only(f):
    @wraps(f)
    def decorated(requestUserId, *args, **kwargs):
        isAdmin = (
            _userColl.find_one({"_id": bson.ObjectId(requestUserId)}, {"role": 1})["role"]
            == "admin"
        )

        if not isAdmin:
            raise UnauthenticatedError("Must be admin!")

        return f(requestUserId, *args, **kwargs)

    return decorated
