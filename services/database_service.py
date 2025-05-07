import pymongo # start [brew services start mongodb/brew/mongodb-community]

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
    
    def read_document(self, db_name: str, collection_name: str, query: dict) -> dict:
        """Reads a document from the specified database and collection."""
        coll = self.connect_to_table(db_name, collection_name)
        return coll.find_one(query)
    
    def update_document(self, db_name: str, collection_name: str, query: dict, update: dict) -> None:
        """Updates a document in the specified database and collection."""
        coll = self.connect_to_table(db_name, collection_name)
        coll.update_one(query, {"$set": update})

    def delete_document(self, db_name: str, collection_name: str, query: dict) -> None:
        """Deletes a document from the specified database and collection."""
        coll = self.connect_to_table(db_name, collection_name)
        coll.delete_one(query)