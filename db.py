from pymongo import MongoClient
from bson import ObjectId


class Database:
    def __init__(self, db_name, mongo_uri):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]

    def insert_document(self, collection_name, document):
        collection = self.db[collection_name]
        collection.insert_one(document)

    def delete_document(self, collection_name, query):
        collection = self.db[collection_name]
        collection.delete_one(query)

    def find_document(self, username, query):
        result = self.db[username].find(query)
        return list(result) if result else []

    def update_document(self, collection_name, query, data):
        collection = self.db[collection_name]
        collection.update_one(query, {'$set': data})

    def get_user_collection(self, username):
        return self.db[username]
