from flask import request, Blueprint
from flaskr.models.Workspace import _workspaceColl
from flaskr.errors.bad_request import BadRequestError
from flaskr.errors.not_found import NotFoundError
from flaskr.errors.unauthenicated import UnauthenticatedError
from datetime import datetime
from flaskr.middlewares.auth import access_token_required
from bson import ObjectId

wsBP = Blueprint("ws", __name__, url_prefix="/api/v1/workspaces")


@wsBP.get("/")
@access_token_required
def getAllWorkspaces(userId):
    wss = _workspaceColl.find({"user_id": ObjectId(userId)}, {"user_id": 0})

    return {"workspaces": list(wss)}



@wsBP.post("/")
@access_token_required
def createWorkspace(userId):
    data = request.json

    if not data or not data.get("title"):
        raise BadRequestError("Please provide data")

    ws_title = data.get("title").strip()

    if not ws_title:
        raise BadRequestError("Title is blank")

    ws = {
        "user_id": ObjectId(userId),
        "title": ws_title,
        "created_at": datetime.now(),
    }

    ws_id = _workspaceColl.insert_one(ws).inserted_id

    new_ws = _workspaceColl.find_one({"_id": ws_id}, {"user_id": 0})

    return {"workspace": new_ws}
