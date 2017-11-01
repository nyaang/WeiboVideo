from pymongo import MongoClient
from values import LOCAL_HOST, PORT


class ConnectDB:
    client = None
    database = None
    collection = None

    def __init__(self, db, cl):
        self.client = MongoClient(LOCAL_HOST, PORT)
        self.database = self.client.get_database(db)
        self.collection = self.database.get_collection(cl)

    def get_handler(self):
        return self.database, self.collection

    def close(self):
        if self.client is not None:
            self.client.close()
