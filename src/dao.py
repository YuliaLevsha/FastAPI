from typing import List, Dict
import pymongo.mongo_client
from pymongo import MongoClient
from src.config import settings


CLIENT: pymongo.mongo_client.MongoClient = MongoClient(settings.mongo_db.mongo_dsn())
DB = CLIENT["FastAPI"]


class DAO:
    def __init__(self, name):
        self.collection = DB[name]

    def create_one(self, data):
        self.collection.insert_one(data)

    def create_many(self, data: List):
        self.collection.insert_many(data)

    def get_one(self, params: Dict) -> Dict:
        return self.collection.find_one(params)

    def get_all(self, params: Dict) -> List[Dict]:
        return self.collection.find(params, {"_id": 0})

    def update(self, document: Dict, data):
        new_data = {"$set": data}
        self.collection.update_one(document, new_data)

    def delete(self, params: Dict):
        self.collection.delete_one(params)

    def check_db(self):
        if len(list(self.get_all({}))):
            return True
        else:
            return False
