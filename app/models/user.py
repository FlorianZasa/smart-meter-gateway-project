from bson.objectid import ObjectId
from flask_bcrypt import generate_password_hash, check_password_hash
from app import db

class User:
    def __init__(self, username, password, role, _id=None):
        self._id = _id
        self.username = username
        self.password = password
        self.role = role

    def save_to_db(self):
        """ Saves the user to the db

        Returns:
            str: The id of the inserted user
        """
        user_data = {
            "username": self.username,
            "password": generate_password_hash(self.password).decode('utf-8'),
            "role": self.role
        }
        if self._id:
            db.users.update_one({"_id": self._id}, {"$set": user_data})
            return str(self._id)
        else:
            result = db.users.insert_one(user_data)
            self._id = result.inserted_id
            return str(result.inserted_id)

    @staticmethod
    def find_by_username(username):
        """ Find user by username

        Args:
            username (str): The username

        Returns:
            User | None: Returns the user
        """
        user_data = db.users.find_one({"username": username})
        if user_data:
            return User(
                username=user_data['username'],
                password=user_data['password'],
                role=user_data['role'],
                _id=user_data['_id']
            )
        return None

    @staticmethod
    def find_by_id(user_id):
        """ Finds the user by user id

        Args:
            user_id (int): User ID

        Returns:
            User | None: The found user
        """
        user_data = db.users.find_one({"_id": ObjectId(user_id)})
        if user_data:
            return User(
                username=user_data['username'],
                password=user_data['password'],
                role=user_data['role'],
                _id=user_data['_id']
            )
        return None

    def check_password(self, password):
        """ Checks if the password is correct

        Args:
            password (str): Password inserted by the user

        Returns:
            bool: Result of the check
        """
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            "id": str(self._id),
            "username": self.username,
            "role": self.role
        }