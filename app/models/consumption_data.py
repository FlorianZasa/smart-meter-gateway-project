from bson.objectid import ObjectId
from datetime import datetime
from app import db

class ConsumptionData:
    def __init__(self, user_id, value, timestamp=None, _id=None):
        self._id = _id
        self.user_id = user_id
        self.value = value
        self.timestamp = timestamp or datetime.utcnow()

    def save_to_db(self):
        data = {
            "user_id": ObjectId(self.user_id),
            "value": self.value,
            "timestamp": self.timestamp
        }
        if self._id:
            db.consumption_data.update_one({"_id": self._id}, {"$set": data})
            return str(self._id)
        else:
            result = db.consumption_data.insert_one(data)
            self._id = result.inserted_id
            return str(result.inserted_id)

    @staticmethod
    def find_by_id(data_id):
        data = db.consumption_data.find_one({"_id": ObjectId(data_id)})
        if data:
            return ConsumptionData(
                user_id=data['user_id'],
                value=data['value'],
                timestamp=data['timestamp'],
                _id=data['_id']
            )
        return None

    @staticmethod
    def find_by_user_id(user_id):
        data_list = db.consumption_data.find({"user_id": ObjectId(user_id)})
        return [ConsumptionData(
                    user_id=data['user_id'],
                    value=data['value'],
                    timestamp=data['timestamp'],
                    _id=data['_id']
                ) for data in data_list]

    def to_dict(self):
        return {
            "id": str(self._id),
            "user_id": str(self.user_id),
            "value": self.value,
            "timestamp": self.timestamp.isoformat()
        }