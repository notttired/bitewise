import pymongo # start [brew services start mongodb/brew/mongodb-community]
from typing import Any

class DatabaseService:
    def __init__(self):
        self.client = client = pymongo.MongoClient("mongodb://localhost:27017/")

    def connect_to_table(self, db_name: str, collection_name: str) -> pymongo.database.Database:
        """Connects to the specified database."""
        return self.client[db_name][collection_name]

    def add_document(self, db_name: str, collection_name: str, document: dict) -> None:
        """Creates a new document in the specified database and collection."""
        coll = self.connect_to_table(db_name, collection_name)
        coll.insert_one(document)

    def add_documents(self, db_name: str, collection_name: str, documents: list[dict]) -> None:
        """Creates multiple documents in the specified database and collection."""
        coll = self.connect_to_table(db_name, collection_name)
        coll.insert_many(documents)

    def read_all_documents(self, db_name: str, collection_name: str) -> list[dict]:
        """Reads all documents from the specified database and collection."""
        coll = self.connect_to_table(db_name, collection_name)
        return list(coll.find())
    
    def read_document(self, db_name: str, collection_name: str, query: dict) -> dict:
        """Reads a document from the specified database and collection."""
        coll = self.connect_to_table(db_name, collection_name)
        return coll.find_one(query)
    
    def read_documents(self, db_name: str, collection_name: str, query: dict) -> list[dict]:
        """Reads multiple documents from the specified database and collection."""
        coll = self.connect_to_table(db_name, collection_name)
        return list(coll.find(query)) # returns pymongo cursor object => convert into list
    
    def read_similar_documents(self, db_name: str, collection_name: str, query: dict) -> list[dict]:
        """Reads similar documents from the specified database and collection."""
        coll = self.connect_to_table(db_name, collection_name)
        query = self.keywords_to_query(query)
        return list(coll.find(query))

    def update_document(self, db_name: str, collection_name: str, query: dict, update: dict) -> None:
        """Updates a document in the specified database and collection."""
        coll = self.connect_to_table(db_name, collection_name)
        coll.update_one(query, {"$set": update})

    def delete_document(self, db_name: str, collection_name: str, query: dict) -> None:
        """Deletes a document from the specified database and collection."""
        coll = self.connect_to_table(db_name, collection_name)
        coll.delete_one(query)

    def delete_all_documents(self, db_name: str, collection_name: str) -> None:
        """Deletes all documents from the specified database and collection."""
        coll = self.connect_to_table(db_name, collection_name)
        coll.delete_many({})

    def keywords_to_query(self, keywords: dict[str, Any]) -> dict[str, Any]:
        """Converts object with values keywords to a query for MongoDB."""
        query = {}
        for key, value in keywords.items():
            if isinstance(value, str):
                query[key] = {"$regex": value, "$options": "i"}
        return query