import os
from pymongo import MongoClient
from pymongo.errors import CollectionInvalid, OperationFailure
from dotenv import load_dotenv

from utils.logger import get_logger

load_dotenv()

logger = get_logger(__name__)

_client = None
_db = None
_collection_ready = False


def get_db():
    global _client, _db
    if _db is None:
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
        db_name = os.getenv("DB_NAME", "smart_expense_tracker")
        _client = MongoClient(mongo_uri)
        _db = _client[db_name]
    return _db


def _expense_collection_validator():
    return {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["amount", "category", "date"],
            "properties": {
                "amount": {
                    "bsonType": ["double", "int", "long", "decimal"],
                    "minimum": 0.01,
                    "description": "amount must be a positive number",
                },
                "category": {
                    "bsonType": "string",
                    "minLength": 1,
                    "description": "category is required",
                },
                "date": {
                    "bsonType": "string",
                    "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$",
                    "description": "date must be ISO format (YYYY-MM-DD)",
                },
                "note": {
                    "bsonType": "string",
                },
                "created_at": {
                    "bsonType": "date",
                },
            },
        }
    }


def _ensure_expenses_collection():
    global _collection_ready
    if _collection_ready:
        return

    db = get_db()
    validator = _expense_collection_validator()

    try:
        # Try to create collection with validator (works with real MongoDB)
        db.create_collection(
            "expenses",
            validator=validator,
            validationLevel="strict",
            validationAction="error",
        )
        logger.info("Created expenses collection with schema validator")
    except (CollectionInvalid, TypeError, AttributeError, NotImplementedError) as e:
        # Collection already exists OR mongomock doesn't support validators
        try:
            db.command(
                {
                    "collMod": "expenses",
                    "validator": validator,
                    "validationLevel": "strict",
                    "validationAction": "error",
                }
            )
            logger.info("Updated expenses collection validator")
        except (OperationFailure, TypeError, AttributeError, NotImplementedError) as exc:
            # mongomock and test environments may not support schema validation
            logger.warning("Could not set collection validator (OK for testing): %s", exc)
            # Still create the collection for testing
            if "expenses" not in db.list_collection_names():
                db.create_collection("expenses")

    db["expenses"].create_index("date")
    db["expenses"].create_index("category")
    _collection_ready = True


def get_expenses_collection():
    _ensure_expenses_collection()
    db = get_db()
    return db["expenses"]
