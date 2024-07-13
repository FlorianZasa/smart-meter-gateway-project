from app import db
from bson.objectid import ObjectId

def get_user_role(user_id):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    return user['role'] if user else None