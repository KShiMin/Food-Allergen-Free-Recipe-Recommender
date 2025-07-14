from pymongo import MongoClient


class MongoCRUD:
    
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["allergen-free-recipes"]
        
    def insert(self, collection, data, ordered=True):
        if isinstance(data, dict):
            return self.db[collection].insert_one(data)
        elif isinstance(data, list):
            return self.db[collection].insert_many(data, ordered=ordered)
        else:
            raise ValueError("Data must be dict or list of dicts.")
        
    def find_one(self, collection, query):
        return self.db[collection].find_one(query)
    
    def find_many(self, collection, query):
        return list(self.db[collection].find(query))
    
    def update_one(self, collection, query, update):
        return self.db[collection].update_one(query, {"$set": update})

    def delete_one(self, collection, query):
        return self.db[collection].delete_one(query)
    
    # Graceful Closing - ensure proper exit
    def __exit__(self, exc_type, exc_value, traceback):
        self.client.close()