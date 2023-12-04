from flask import request, Blueprint, jsonify
import jwt
import os
from werkzeug.security import generate_password_hash, check_password_hash
import bson
from flaskr.models.User import _userColl
from flaskr.errors.bad_request import BadRequestError
from flaskr.errors.not_found import NotFoundError
from flaskr.errors.unauthenicated import UnauthenticatedError
import re
from datetime import datetime, timezone, timedelta
from flaskr.middlewares.auth import access_token_required

authBP = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@authBP.post("/login")
def login():
    data = request.form
    if not data:
        raise BadRequestError("Please provide data")

    email = data.get("email")
    password = data.get("password")

    if not email or not password or not re.match(r"^[\w\.-]+@[\w\.-]+$", email.strip()):
        raise BadRequestError("Invalid data")

    email = email.strip()
    password = password.strip()

    user = _userColl.find_one({"email": email})

    if user and check_password_hash(user["hash_password"], password):
        user["_id"] = str(user["_id"])
        token = jwt.encode(
            {
                "user_id": user["_id"],
                "exp": datetime.now(tz=timezone.utc)
                + timedelta(days=int(os.getenv("JWT_LIFETIME"))),
            },
            os.getenv("JWT_SECRET"),
            algorithm="HS256",
        )
        return jsonify(
            user_id=user["_id"],
            username=user["username"],
            role=user["role"],
            access_token=token,
        )
    raise UnauthenticatedError("Invalid email or password")


@authBP.post("/register")
def register():
    data = request.form
    if not data:
        raise BadRequestError("Please provide data")

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if (
        not username
        or not email
        or not password
        or not re.match(r"^[\w\.-]+@[\w\.-]+$", email.strip())
    ):
        raise BadRequestError("Invalid data")

    username = username.strip()
    email = email.strip()
    password = password.strip()

    if _userColl.find_one(
        {
            "$or": [
                {"username": username},
                {"email": email},
            ]
        }
    ):
        raise BadRequestError("User already exist")

    newUser = _userColl.insert_one(
        {
            "username": username,
            "email": email,
            "hash_password": generate_password_hash(password),
            "role": "user",
            "created_at": datetime.now(),
        }
    )
    newUser = _userColl.find_one({"_id": newUser.inserted_id})

    return jsonify(
        user_id=str(newUser["_id"]),
        username=newUser["username"],
        role=newUser["role"],
    )


@authBP.post("/testAuth")
@access_token_required
def testAuth(user):
    return jsonify(user)
