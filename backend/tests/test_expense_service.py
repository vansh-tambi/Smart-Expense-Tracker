"""
Unit tests for expense_service module.
Tests business logic for expense CRUD operations.
"""
import pytest
from datetime import datetime
from bson import ObjectId
from mongomock import MongoClient


class TestCreateExpense:
    """Test expense creation logic."""

    def test_create_valid_expense(self, monkeypatch):
        """Test creating a valid expense."""
        # Setup mocked database
        mock_mongo = MongoClient()
        db = mock_mongo["test_smart_expense_tracker"]
        
        # Monkeypatch get_expenses_collection
        import models.db
        models.db._db = db
        models.db._collection_ready = False
        
        from services import expense_service
        
        data = {
            "amount": 25.50,
            "category": "Food",
            "date": "2024-04-15",
            "note": "Lunch",
        }
        
        result = expense_service.create_expense(data)
        
        assert result["amount"] == 25.50
        assert result["category"] == "Food"
        assert result["date"] == "2024-04-15"
        assert result["note"] == "Lunch"
        assert "id" in result
        assert "created_at" in result

    def test_create_expense_rejects_zero_amount(self):
        """Test that zero amount is rejected even in service."""
        from pydantic import ValidationError
        from services import expense_service
        
        data = {
            "amount": 0,
            "category": "Food",
        }
        
        with pytest.raises(ValidationError):
            expense_service.create_expense(data)

    def test_create_expense_rejects_negative_amount(self):
        """Test that negative amount is rejected."""
        from pydantic import ValidationError
        from services import expense_service
        
        data = {
            "amount": -10.00,
            "category": "Food",
        }
        
        with pytest.raises(ValidationError):
            expense_service.create_expense(data)

    def test_create_expense_rejects_invalid_category(self):
        """Test that invalid category is rejected."""
        from pydantic import ValidationError
        from services import expense_service
        
        data = {
            "amount": 25.00,
            "category": "InvalidCategory",
        }
        
        with pytest.raises(ValidationError):
            expense_service.create_expense(data)


class TestGetAllExpenses:
    """Test retrieving all expenses."""

    def test_get_all_expenses_empty(self):
        """Test getting expenses when collection is empty."""
        from mongomock import MongoClient
        import models.db
        
        mock_mongo = MongoClient()
        db = mock_mongo["test_smart_expense_tracker"]
        models.db._db = db
        models.db._collection_ready = False
        
        from services import expense_service
        expenses = expense_service.get_all_expenses()
        assert expenses == []

    def test_get_all_expenses_sorted_by_date(self):
        """Test that expenses are sorted by date descending."""
        from mongomock import MongoClient
        import models.db
        from services import expense_service
        
        mock_mongo = MongoClient()
        db = mock_mongo["test_smart_expense_tracker"]
        models.db._db = db
        models.db._collection_ready = False
        
        # Insert unsorted expenses
        db.expenses.insert_many([
            {"amount": 10.00, "category": "Food", "date": "2024-04-10", "note": "", "created_at": datetime.now()},
            {"amount": 20.00, "category": "Food", "date": "2024-04-20", "note": "", "created_at": datetime.now()},
            {"amount": 15.00, "category": "Food", "date": "2024-04-15", "note": "", "created_at": datetime.now()},
        ])
        
        expenses = expense_service.get_all_expenses()
        
        assert len(expenses) == 3
        # Should be sorted by date descending
        assert expenses[0]["date"] == "2024-04-20"
        assert expenses[1]["date"] == "2024-04-15"
        assert expenses[2]["date"] == "2024-04-10"

    def test_get_all_expenses_serialize_id(self):
        """Test that MongoDB _id is converted to string 'id' field."""
        from mongomock import MongoClient
        import models.db
        from services import expense_service
        
        mock_mongo = MongoClient()
        db = mock_mongo["test_smart_expense_tracker"]
        models.db._db = db
        models.db._collection_ready = False
        
        db.expenses.insert_one({
            "amount": 25.00,
            "category": "Food",
            "date": "2024-04-15",
            "note": "",
            "created_at": datetime.now(),
        })
        
        expenses = expense_service.get_all_expenses()
        
        assert len(expenses) == 1
        assert "id" in expenses[0]
        assert "_id" not in expenses[0]
        assert isinstance(expenses[0]["id"], str)


class TestGetCategorySummary:
    """Test category-wise spending summary."""

    def test_category_summary_empty(self):
        """Test summary when no expenses exist."""
        from mongomock import MongoClient
        import models.db
        from services import expense_service
        
        mock_mongo = MongoClient()
        db = mock_mongo["test_smart_expense_tracker"]
        models.db._db = db
        models.db._collection_ready = False
        
        summary = expense_service.get_category_summary()
        assert summary == []

    def test_category_summary_single_expense(self):
        """Test summary with a single expense."""
        from mongomock import MongoClient
        import models.db
        from services import expense_service
        
        mock_mongo = MongoClient()
        db = mock_mongo["test_smart_expense_tracker"]
        models.db._db = db
        models.db._collection_ready = False
        
        db.expenses.insert_one({
            "amount": 25.50,
            "category": "Food",
            "date": "2024-04-15",
            "note": "",
            "created_at": datetime.now(),
        })
        
        summary = expense_service.get_category_summary()
        
        assert len(summary) == 1
        assert summary[0]["category"] == "Food"
        assert summary[0]["total"] == 25.50
        assert summary[0]["count"] == 1

    def test_category_summary_multiple_categories(self):
        """Test summary with multiple categories."""
        from mongomock import MongoClient
        import models.db
        from services import expense_service
        
        mock_mongo = MongoClient()
        db = mock_mongo["test_smart_expense_tracker"]
        models.db._db = db
        models.db._collection_ready = False
        
        db.expenses.insert_many([
            {"amount": 25.00, "category": "Food", "date": "2024-04-15", "note": "", "created_at": datetime.now()},
            {"amount": 15.00, "category": "Food", "date": "2024-04-14", "note": "", "created_at": datetime.now()},
            {"amount": 100.00, "category": "Transport", "date": "2024-04-15", "note": "", "created_at": datetime.now()},
            {"amount": 50.00, "category": "Shopping", "date": "2024-04-13", "note": "", "created_at": datetime.now()},
        ])
        
        summary = expense_service.get_category_summary()
        
        # Should be sorted by total descending
        assert len(summary) == 3
        assert summary[0]["category"] == "Transport"
        assert summary[0]["total"] == 100.00
        assert summary[1]["category"] == "Food"
        assert summary[1]["total"] == 40.00
        assert summary[2]["category"] == "Shopping"
        assert summary[2]["total"] == 50.00

    def test_category_summary_aggregates_count(self):
        """Test that count is aggregated correctly."""
        from mongomock import MongoClient
        import models.db
        from services import expense_service
        
        mock_mongo = MongoClient()
        db = mock_mongo["test_smart_expense_tracker"]
        models.db._db = db
        models.db._collection_ready = False
        
        db.expenses.insert_many([
            {"amount": 10.00, "category": "Food", "date": "2024-04-15", "note": "", "created_at": datetime.now()},
            {"amount": 20.00, "category": "Food", "date": "2024-04-14", "note": "", "created_at": datetime.now()},
            {"amount": 15.00, "category": "Food", "date": "2024-04-13", "note": "", "created_at": datetime.now()},
        ])
        
        summary = expense_service.get_category_summary()
        
        assert summary[0]["category"] == "Food"
        assert summary[0]["total"] == 45.00
        assert summary[0]["count"] == 3

    def test_category_summary_sorted_by_total(self):
        """Test that summary is sorted by total descending."""
        from mongomock import MongoClient
        import models.db
        from services import expense_service
        
        mock_mongo = MongoClient()
        db = mock_mongo["test_smart_expense_tracker"]
        models.db._db = db
        models.db._collection_ready = False
        
        db.expenses.insert_many([
            {"amount": 5.00, "category": "Food", "date": "2024-04-15", "note": "", "created_at": datetime.now()},
            {"amount": 100.00, "category": "Shopping", "date": "2024-04-15", "note": "", "created_at": datetime.now()},
            {"amount": 50.00, "category": "Entertainment", "date": "2024-04-15", "note": "", "created_at": datetime.now()},
        ])
        
        summary = expense_service.get_category_summary()
        
        assert summary[0]["total"] == 100.00
        assert summary[1]["total"] == 50.00
        assert summary[2]["total"] == 5.00


class TestDeleteExpense:
    """Test expense deletion logic."""

    def test_delete_existing_expense(self):
        """Test deleting an existing expense."""
        from mongomock import MongoClient
        import models.db
        from services import expense_service
        
        mock_mongo = MongoClient()
        db = mock_mongo["test_smart_expense_tracker"]
        models.db._db = db
        models.db._collection_ready = False
        
        doc_id = ObjectId()
        db.expenses.insert_one({
            "_id": doc_id,
            "amount": 25.00,
            "category": "Food",
            "date": "2024-04-15",
            "note": "",
            "created_at": datetime.now(),
        })
        
        deleted = expense_service.delete_expense(str(doc_id))
        
        assert deleted is not None
        assert deleted["id"] == str(doc_id)
        assert deleted["amount"] == 25.00
        
        # Verify it's actually deleted
        assert db.expenses.find_one({"_id": doc_id}) is None

    def test_delete_nonexistent_expense(self):
        """Test deleting an expense that doesn't exist."""
        from mongomock import MongoClient
        import models.db
        from services import expense_service
        
        mock_mongo = MongoClient()
        db = mock_mongo["test_smart_expense_tracker"]
        models.db._db = db
        models.db._collection_ready = False
        
        fake_id = str(ObjectId())
        deleted = expense_service.delete_expense(fake_id)
        
        assert deleted is None

    def test_delete_invalid_id_format(self):
        """Test deleting with invalid ObjectId format."""
        from mongomock import MongoClient
        import models.db
        from services import expense_service
        
        mock_mongo = MongoClient()
        db = mock_mongo["test_smart_expense_tracker"]
        models.db._db = db
        models.db._collection_ready = False
        
        deleted = expense_service.delete_expense("not-a-valid-id")
        
        assert deleted is None
