from flask import request, Blueprint
from flaskr.errors.bad_request import BadRequestError

from flaskr.models.Post import _postColl
from flaskr.models.Workspace import _workspaceColl
from bson.objectid import ObjectId

from datetime import datetime


postBP = Blueprint("post", __name__, url_prefix="/api/v1/posts")

@postBP.post("/")
def createPost():
    data = request.json
    if not data:
        raise BadRequestError("Please provide data")
    
    workspaceId = ObjectId(data.get("workspaceId"))
    if not _workspaceColl.find_one({"_id": workspaceId}):
        raise BadRequestError("Invalid data")
    
    post = {
        "workspace_id": workspaceId,
        "title": data.get("title"),
        "pos": data.get("pos"),
        "created_at": datetime.now()
    }

    post_id = _postColl.insert_one(post).inserted_id
    new_post = _postColl.find_one({"_id": post_id})
    return {"post": new_post}

    

@postBP.get("/")
def getPosts():
    workspaceId = ObjectId(request.args.get("workspaceId"))
    posts = _postColl.find({"workspace_id": workspaceId})
    if not posts:
        raise BadRequestError("Invalid data")
    return {
        "posts": list(posts)
    }

@postBP.get("/<string:postId>")
def getPost(postId):
    post_Id = ObjectId(postId)
    post = _postColl.find_one({"_id": post_Id})
    if not post:
        raise BadRequestError("Invalid data")
    return {"post": post}

@postBP.put("/<string:postId>")
def updatePost(postId):
    update_data = request.json
    if not update_data:
        raise BadRequestError("Please provide data")
    
    post_Id = ObjectId(postId)
    post = _postColl.find_one({"_id": post_Id})
    if not post:
        raise BadRequestError("Invalid data")
    result = _postColl.update_one({"_id": post_Id}, {"$set": update_data})
    updatePost = _postColl.find_one({"_id": post_Id})
    print(result)
    return {
        "post": updatePost
    }

@postBP.delete("/<string:postId>")
def deletePost(postId):
    post_Id = ObjectId(postId)
    if not _postColl.find_one({"_id": post_Id}):
        raise BadRequestError("Invalid data")

    result = _postColl.delete_one({"_id": post_Id})
    return {
        "status": "Delete Successfuly"
    }    


    


