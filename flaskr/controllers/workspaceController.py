from flask import request, Blueprint
from flaskr.models.Workspace import _workspaceColl
from flaskr.errors.bad_request import BadRequestError
from flaskr.errors.not_found import NotFoundError
from flaskr.errors.unauthenicated import UnauthenticatedError
from datetime import datetime
from flaskr.middlewares.auth import access_token_required

wsBP = Blueprint("ws", __name__, url_prefix="/api/v1/workspace")


@wsBP.get("/")
@access_token_required
def getAllWorkspaces(user):
    wss = _workspaceColl.find({"user_id": user["_id"]}, {"user_id": 0})

    return {"workspaces": list(wss)}



@wsBP.post("/")
@access_token_required
def createWorkspace(user):
    data = request.json

    if not data or not data.get("title"):
        raise BadRequestError("Please provide data")

    ws_title = data.get("title").strip()

    if not ws_title:
        raise BadRequestError("Title is blank")

    ws = {
        "user_id": user["_id"],
        "title": ws_title,
        "created_at": datetime.now(),
    }

    ws_id = _workspaceColl.insert_one(ws).inserted_id

    new_ws = _workspaceColl.find_one({"_id": ws_id}, {"user_id": 0})

    return {"workspace": new_ws}
