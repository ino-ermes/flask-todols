from flask import request, Blueprint
from bson.objectid import ObjectId

from flaskr.errors.bad_request import BadRequestError

from datetime import datetime

from flaskr.models.Tag import _tagColl

tagBP = Blueprint("tag", __name__, url_prefix="/api/v1/tags")

@tagBP.post("/")
def createTag():
    data = request.json
    if not data:
        raise BadRequestError("Please provide data")
    
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
def updateTag(tagId):
    update_data = request.json
    if not update_data:
        raise BadRequestError("Please provide data")
    
    tag_Id = ObjectId(tagId)
    post = _tagColl.find_one({"_id": tag_Id})
    if not post:
        raise BadRequestError("Invalid data")
    result = _tagColl.update_one({"_id": tag_Id}, {"$set": update_data})
    updateTag = _tagColl.find_one({"_id": tag_Id})
    return {
        "tag": updateTag
    }

@tagBP.delete("/<string:tagId>")
def deleteTag(tagId):
    if not tagId:
        raise BadRequestError("Invalid data")
    
    tag_Id = ObjectId(tagId)
    if not _tagColl.delete_one({"_id": tag_Id}):
        raise BadRequestError("Invalid data")
    
    return {"status": "delete Successfuly"}