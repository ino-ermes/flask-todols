from flaskr.db import db

database = db.getDB()

_postColl = None

try:
    _postColl = database.create_collection("post")
except:
    _postColl = database.get_collection("post")

post_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["workspace_id", "title", "pos", "created_at"],
        "properties": {
            "workspace_id": {
                "bsonType": "objectId",
                "description": "must be an objectid and is required",
            },
            "title": {
                "bsonType": "string",
                "description": "must be a string and is required",
            },
            "pos": {
                "bsonType": "integer",
                "description": "must be a integer and is required",
            },
            "created_at": {
                "bsonType": "date",
                "description": "must be a date and is required",
            },
        },
    }
}

database.command("collMod", "post", validator=post_validator)
