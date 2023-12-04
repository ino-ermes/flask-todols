from functools import wraps
import jwt
from flask import request
import bson, os
from flaskr.db import db
from flaskr.errors.unauthenicated import UnauthenticatedError

__userColl = db.getDB().user

def access_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            raise UnauthenticatedError('Authentication Token is missing!')
        
        data = jwt.decode(
            token, os.getenv('JWT_SECRET'), algorithms=["HS256"]
        )
        current_user = __userColl.find_one({'_id': bson.ObjectId(data["user_id"])})

        if current_user is None:
            raise UnauthenticatedError('Invalid Authentication token!')

        current_user["_id"] = str(current_user["_id"])
        current_user["hash_password"] = "hidden"

        return f(current_user, *args, **kwargs)

    return decorated
