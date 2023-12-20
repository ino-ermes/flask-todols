from flask import request, Blueprint
from flaskr.errors.bad_request import BadRequestError

from flaskr.models.Post import _postColl
from flaskr.models.Workspace import _workspaceColl
from bson.objectid import ObjectId

from datetime import datetime
from flaskr.middlewares.auth import access_token_required


postBP = Blueprint("post", __name__, url_prefix="/api/v1/posts")

@postBP.post("/")
@access_token_required
def createPost(user):
    data = request.json
    if not data:
        raise BadRequestError("Please provide data")
    
    workspaceId = ObjectId(data.get("workspaceId"))
    workspace = _workspaceColl.find_one({"_id": workspaceId})
    if not workspace:
        raise BadRequestError("Invalid data")
    
    if workspace["user_id"] != user["_id"]:
        raise BadRequestError("Permission denied!")

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
@access_token_required
def updatePost(user, postId):
    print(user)
    update_data = request.json
    if not update_data:
        raise BadRequestError("Please provide data")
    
    update_data.pop("workspace_id", None)
    
    post_Id = ObjectId(postId)
    post = _postColl.find_one({"_id": post_Id})
    workspace = _workspaceColl.find_one({"_id": post["workspace_id"]})
    if workspace["user_id"] != user["_id"]:
        raise BadRequestError("Permission denied!")
    
    if not post:
        raise BadRequestError("Invalid data")
    result = _postColl.update_one({"_id": post_Id}, {"$set": update_data})
    updatePost = _postColl.find_one({"_id": post_Id})
    print(result)
    return {
        "post": updatePost
    }

@postBP.delete("/<string:postId>")
@access_token_required
def deletePost(user, postId):
    post_Id = ObjectId(postId)
    post = _postColl.find_one({"_id": post_Id})
    if not post:
        raise BadRequestError("Invalid data")
    
    workspace = _workspaceColl.find_one({"_id": post["workspace_id"]})
    if workspace["user_id"] != user["_id"]:
        raise BadRequestError("Permission denied!")

    result = _postColl.delete_one({"_id": post_Id})
    return {
        "status": "Delete Successfuly"
    }
