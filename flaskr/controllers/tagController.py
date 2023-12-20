from flask import request, Blueprint
from bson.objectid import ObjectId

from flaskr.errors.bad_request import BadRequestError

from datetime import datetime
from flaskr.middlewares.auth import access_token_required
from flaskr.models.Tag import _tagColl
from flaskr.models.Post import _postColl
from flaskr.models.Workspace import _workspaceColl

tagBP = Blueprint("tag", __name__, url_prefix="/api/v1/tags")

@tagBP.post("/")
@access_token_required
def createTag(user):
    data = request.json
    if not data:
        raise BadRequestError("Please provide data")
    
    post = _postColl.find_one({"_id": ObjectId(data.get("post_id"))})
    if not post:
        raise BadRequestError("Invalid data")
    
    workspace = _workspaceColl.find_one({"_id": post["workspace_id"]})
    if workspace["user_id"] != user["_id"]:
        raise BadRequestError("Permission denied!")
    
    tag = {
        "post_id": ObjectId(data.get("post_id")),
        "title": data.get("title"),
        "category": data.get("category"),
        "body": data.get("body"),
        "status": data.get("status"),
        "deadline": datetime.strptime(data.get("deadline"), "%Y-%m-%dT%H:%M:%S"),
        "pos": data.get("pos"), 
        "created_at": datetime.now()
    }

    tag_id = _tagColl.insert_one(tag).inserted_id
    new_tag = _tagColl.find_one({"_id": tag_id})
    return {"tag": new_tag}

@tagBP.get("/")
def tag():
    post_id = ObjectId(request.args.get("postId"))
    if not post_id:
        raise BadRequestError("Invalid data")
    
    tag = _tagColl.find_one({"post_id": post_id})
    
    return {"tag": tag}
    
@tagBP.get("/<string:tagId>")
def getTag(tagId):
    if not tagId:
        raise BadRequestError("Invalid data")
    tag_Id = ObjectId(tagId)
    tag = _tagColl.find_one({"_id": tag_Id})
    if not tag:
        raise BadRequestError("Invalid data")
    
    return {"tag": tag}

@tagBP.put("/<string:tagId>")
@access_token_required
def updateTag(user, tagId):
    update_data = request.json
    if not update_data:
        raise BadRequestError("Please provide data")
    
    tag_Id = ObjectId(tagId)
    post = _postColl.find_one({"_id": tag_Id})
    if not post:
        raise BadRequestError("Invalid data")
    workspace = _workspaceColl.find_one({"_id": post["workspace_id"]})
    if workspace["user_id"] != user["_id"]:
        raise BadRequestError("Permission denied!")

    result = _tagColl.update_one({"_id": tag_Id}, {"$set": update_data})
    updateTag = _tagColl.find_one({"_id": tag_Id})
    return {
        "tag": updateTag
    }

@tagBP.delete("/<string:tagId>")
@access_token_required
def deleteTag(user, tagId):
    if not tagId:
        raise BadRequestError("Invalid data")
    
    tag_Id = ObjectId(tagId)
    tag = _tagColl.find_one({"_id": tag_Id})
    post = _postColl.find_one({"_id": tag["post_id"]})
    workspace = _workspaceColl.find_one({"_id": post["workspace_id"]})
    if workspace["user_id"] != user["_id"]:
        raise BadRequestError("Permission denied!")
    if not _tagColl.delete_one({"_id": tag_Id}):
        raise BadRequestError("Invalid data")
    return {"status": "delete Successfuly"}