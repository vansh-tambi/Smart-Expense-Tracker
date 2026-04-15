import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

_client = None
_db = None


def get_db():
    global _client, _db
    if _db is None:
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
        db_name = os.getenv("DB_NAME", "smart_expense_tracker")
        _client = MongoClient(mongo_uri)
        _db = _client[db_name]
    return _db


def get_expenses_collection():
    db = get_db()
    return db["expenses"]
