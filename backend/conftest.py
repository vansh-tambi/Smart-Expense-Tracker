"""
Pytest configuration and fixtures for Smart Expense Tracker.
"""
import os
import pytest
from mongomock import MongoClient
from app import create_app
from models.db import get_db
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.fixture
def mock_mongo():
    """Fixture to provide a mocked MongoDB client."""
    return MongoClient()


@pytest.fixture
def client(mock_mongo, monkeypatch):
    """
    Flask test client with mocked MongoDB.
    Cleans up the test database after each test.
    """
    # Monkeypatch the MongoDB connection to use mongomock
    monkeypatch.setenv("MONGO_URI", "")  # mongomock ignores URI
    monkeypatch.setenv("DB_NAME", "test_smart_expense_tracker")

    # Mock get_db to return mongomock database
    def mock_get_db():
        return mock_mongo["test_smart_expense_tracker"]

    # Patch the module-level get_db function
    import models.db
    original_get_db = models.db.get_db
    models.db.get_db = mock_get_db

    # Create Flask app
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client

    # Cleanup
    models.db.get_db = original_get_db
    models.db._db = None
    models.db._client = None
    models.db._collection_ready = False


@pytest.fixture
def sample_expense():
    """Sample valid expense data."""
    return {
        "amount": 25.50,
        "category": "Food",
        "date": "2024-04-15",
        "note": "Lunch at office",
    }


@pytest.fixture
def expenses_list(mock_mongo):
    """
    Pre-populate test database with sample expenses.
    Returns the list of expense documents.
    """
    db = mock_mongo["test_smart_expense_tracker"]
    expenses = [
        {
            "amount": 25.50,
            "category": "Food",
            "date": "2024-04-15",
            "note": "Lunch",
        },
        {
            "amount": 50.00,
            "category": "Transport",
            "date": "2024-04-15",
            "note": "Uber ride",
        },
        {
            "amount": 100.00,
            "category": "Shopping",
            "date": "2024-04-14",
            "note": "Clothes",
        },
        {
            "amount": 15.00,
            "category": "Food",
            "date": "2024-04-14",
            "note": "Coffee",
        },
        {
            "amount": 200.00,
            "category": "Entertainment",
            "date": "2024-04-13",
            "note": "Concert tickets",
        },
    ]
    result = db.expenses.insert_many(expenses)
    expenses_with_ids = [
        {**doc, "_id": str(doc_id)} for doc, doc_id in zip(expenses, result.inserted_ids)
    ]
    return expenses_with_ids
