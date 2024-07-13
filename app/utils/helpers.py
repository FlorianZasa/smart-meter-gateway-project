from app import db
from bson.objectid import ObjectId

def get_user_role(user_id):
    """ Extracts the user role from id

    Args:
        user_id (int): The ID of the user from the db

    Returns:
        role | None: User role or None
    """
    user = db.users.find_one({"_id": ObjectId(user_id)})
    return user['role'] if user else None