from flask import request, Blueprint
from bson.objectid import ObjectId

from flaskr.errors.bad_request import BadRequestError
from flaskr.errors.forbidden import ForbiddenError

from datetime import datetime, date
from flaskr.middlewares.auth import access_token_required
from flaskr.models.Tag import _tagColl
from flaskr.models.Post import _postColl
from flaskr.models.Workspace import _workspaceColl
import isodate as iso
tagBP = Blueprint("tag", __name__, url_prefix="/api/v1/tags")


@tagBP.post("/")
@access_token_required
def createTag(requestUserId):
    data = request.json
    if not data:
        raise BadRequestError("Please provide data")

    try:
        workspace_id = _postColl.find_one({"_id": ObjectId(data.get("post_id"))}, {"workspace_id": 1})["workspace_id"]
        userId = _workspaceColl.find_one({"_id": workspace_id}, {"user_id": 1})["user_id"]
    except:
        raise BadRequestError("Invalid data")

    if userId != requestUserId:
        raise ForbiddenError("Permission denied!")

    tag = {
        "post_id": ObjectId(data.get("post_id")),
        "title": data.get("title"),
        "category": data.get("category"),
        "body": data.get("body"),
        "status": data.get("status"),
        "deadline": datetime.strptime(data.get("deadline"), "%Y/%m/%d"),
        "pos": data.get("pos"),
        "created_at": datetime.now(),
    }

    tag_id = _tagColl.insert_one(tag).inserted_id
    new_tag = _tagColl.find_one({"_id": tag_id})
    return {"tag": new_tag}


@tagBP.get("/")
@access_token_required
def getAllTags(requestUserId):
    post_id = request.args.get("postId")
    if not post_id:
        raise BadRequestError("Invalid data")

    try:
        workspace_id = _postColl.find_one({"_id": ObjectId(post_id)}, {"workspace_id": 1})["workspace_id"]
        userId = _workspaceColl.find_one({"_id": workspace_id}, {"user_id": 1})["user_id"]
    except:
        raise BadRequestError("Invalid data")

    if userId != requestUserId:
        raise ForbiddenError("Permission denied!")
    
    tags = _tagColl.aggregate(
        [
            {
                "$match": {"post_id": ObjectId(post_id)},
            },
            {
                "$sort": {
                    "pos": 1,
                },
            },
        ]
    )

    return {"tag": list(tags)}


@tagBP.get("/<tagId>")
@access_token_required
def getTag(requestUserId, tagId):
    if not tagId:
        raise BadRequestError("Invalid data")

    tag = _tagColl.find_one({"_id": ObjectId(tagId)})
    if not tag:
        raise BadRequestError("Invalid data")

    post = _postColl.find_one({"_id": tag["post_id"]}, {"workspace_id": 1})
    try:
        userId = _workspaceColl.find_one({"_id": post["workspace_id"]}, {"user_id": 1})["user_id"]
    except:
        raise BadRequestError("Invalid data")
    if userId != requestUserId:
        raise ForbiddenError("Permission denied!")

    return {"tag": tag}


@tagBP.put("/<tagId>")
@access_token_required
def updateTag(requestUserId, tagId):
    data = request.json
    if not data:
        raise BadRequestError("Please provide data")

    if not tagId:
        raise BadRequestError("Invalid data")

    tag = _tagColl.find_one({"_id": ObjectId(tagId)})
    if not tag:
        raise BadRequestError("Invalid data")

    post = _postColl.find_one({"_id": tag["post_id"]}, {"workspace_id": 1})
    try:
        userId = _workspaceColl.find_one({"_id": post["workspace_id"]}, {"user_id": 1})["user_id"]
    except:
        raise BadRequestError("Invalid data")
    if userId != requestUserId:
        raise ForbiddenError("Permission denied!")
    
    updateTag = {
        "title": data.get("title"),
        "category": data.get("category"),
        "body": data.get("body"),
        "status": data.get("status"),
        "deadline": datetime.strptime(data.get("deadline"), "%Y/%m/%d"),
        "pos": data.get("pos"),
    }

    updatedTag = _tagColl.find_one_and_update(
        {"_id": ObjectId(tagId)}, {"$set": updateTag}, return_document=True
    )
    return {"tag": updatedTag}


@tagBP.delete("/<tagId>")
@access_token_required
def deleteTag(requestUserId, tagId):
    if not tagId:
        raise BadRequestError("Invalid data")

    tag = _tagColl.find_one({"_id": ObjectId(tagId)})
    if not tag:
        raise BadRequestError("Invalid data")

    post = _postColl.find_one({"_id": tag["post_id"]}, {"workspace_id": 1})
    userId = _workspaceColl.find_one({"_id": post["workspace_id"]}, {"user_id": 1})[
        "user_id"
    ]
    if userId != requestUserId:
        raise ForbiddenError("Permission denied!")

    _tagColl.delete_one({"_id": ObjectId(tagId)})
    return {"message": "Deleted Successfully"}
