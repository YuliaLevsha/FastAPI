from src.config import settings
from typing import List, Dict
from pymongo import MongoClient


CLIENT = MongoClient(settings.mongo_db.mongo_dsn())
DB = CLIENT['FastAPI']


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
        return self.collection.find(params)

    def update(self, params: Dict, data):
        document = self.get_one(params)
        new_data = {'$set': data}
        self.collection.update_one(document, new_data)

    def delete(self, params: Dict):
        self.collection.delete_one(params)
