"""
Integration tests for Flask API endpoints.
Tests all REST routes with realistic data flows.
"""
import pytest
import json
from datetime import datetime


class TestAddExpenseEndpoint:
    """Test POST /api/expenses/ endpoint."""

    def test_add_expense_success(self, client, sample_expense):
        """Test successfully adding a valid expense."""
        response = client.post(
            "/api/expenses/",
            data=json.dumps(sample_expense),
            content_type="application/json",
        )
        
        assert response.status_code == 201
        data = response.get_json()
        assert data["success"] is True
        assert data["data"]["amount"] == sample_expense["amount"]
        assert data["data"]["category"] == sample_expense["category"]
        assert data["data"]["date"] == sample_expense["date"]
        assert "id" in data["data"]

    def test_add_expense_minimal_fields(self, client):
        """Test adding expense with only required fields."""
        expense = {
            "amount": 50.00,
            "category": "Transport",
        }
        
        response = client.post(
            "/api/expenses/",
            data=json.dumps(expense),
            content_type="application/json",
        )
        
        assert response.status_code == 201
        data = response.get_json()
        assert data["success"] is True
        # Date should default to today
        today = datetime.now().strftime("%Y-%m-%d")
        assert data["data"]["date"] == today
        assert data["data"]["note"] == ""

    def test_add_expense_zero_amount_fails(self, client):
        """Test that zero amount is rejected."""
        expense = {
            "amount": 0,
            "category": "Food",
        }
        
        response = client.post(
            "/api/expenses/",
            data=json.dumps(expense),
            content_type="application/json",
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data or "validation" in data.get("error", "").lower()

    def test_add_expense_negative_amount_fails(self, client):
        """Test that negative amount is rejected."""
        expense = {
            "amount": -25.00,
            "category": "Food",
        }
        
        response = client.post(
            "/api/expenses/",
            data=json.dumps(expense),
            content_type="application/json",
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_add_expense_missing_amount_fails(self, client):
        """Test that missing amount is rejected."""
        expense = {
            "category": "Food",
        }
        
        response = client.post(
            "/api/expenses/",
            data=json.dumps(expense),
            content_type="application/json",
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data or "details" in data

    def test_add_expense_missing_category_fails(self, client):
        """Test that missing category is rejected."""
        expense = {
            "amount": 25.00,
        }
        
        response = client.post(
            "/api/expenses/",
            data=json.dumps(expense),
            content_type="application/json",
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_add_expense_invalid_category_fails(self, client):
        """Test that invalid category is rejected."""
        expense = {
            "amount": 25.00,
            "category": "InvalidCategory",
        }
        
        response = client.post(
            "/api/expenses/",
            data=json.dumps(expense),
            content_type="application/json",
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_add_expense_invalid_date_fails(self, client):
        """Test that invalid date format is rejected."""
        expense = {
            "amount": 25.00,
            "category": "Food",
            "date": "04/15/2024",  # Wrong format
        }
        
        response = client.post(
            "/api/expenses/",
            data=json.dumps(expense),
            content_type="application/json",
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data


class TestListExpensesEndpoint:
    """Test GET /api/expenses/ endpoint."""

    def test_list_expenses_empty(self, client):
        """Test listing expenses when none exist."""
        response = client.get("/api/expenses/")
        
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert data["data"] == []
        assert data["count"] == 0

    def test_list_expenses_returns_all(self, client, mock_mongo):
        """Test listing all expenses."""
        # Setup: insert sample data
        db = mock_mongo["test_smart_expense_tracker"]
        db.expenses.insert_many([
            {"amount": 25.00, "category": "Food", "date": "2024-04-15", "note": "", "created_at": datetime.now()},
            {"amount": 50.00, "category": "Transport", "date": "2024-04-15", "note": "", "created_at": datetime.now()},
            {"amount": 100.00, "category": "Shopping", "date": "2024-04-14", "note": "", "created_at": datetime.now()},
        ])
        
        response = client.get("/api/expenses/")
        
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert data["count"] == 3
        assert len(data["data"]) == 3

    def test_list_expenses_sorted_by_date(self, client, mock_mongo):
        """Test that expenses are returned sorted by date descending."""
        db = mock_mongo["test_smart_expense_tracker"]
        db.expenses.insert_many([
            {"amount": 10.00, "category": "Food", "date": "2024-04-10", "note": "", "created_at": datetime.now()},
            {"amount": 30.00, "category": "Food", "date": "2024-04-30", "note": "", "created_at": datetime.now()},
            {"amount": 20.00, "category": "Food", "date": "2024-04-20", "note": "", "created_at": datetime.now()},
        ])
        
        response = client.get("/api/expenses/")
        
        assert response.status_code == 200
        data = response.get_json()
        expenses = data["data"]
        
        # Should be sorted descending: 04-30, 04-20, 04-10
        assert expenses[0]["date"] == "2024-04-30"
        assert expenses[1]["date"] == "2024-04-20"
        assert expenses[2]["date"] == "2024-04-10"

    def test_list_expenses_includes_id(self, client, mock_mongo):
        """Test that response includes 'id' field (not _id)."""
        db = mock_mongo["test_smart_expense_tracker"]
        db.expenses.insert_one({
            "amount": 25.00,
            "category": "Food",
            "date": "2024-04-15",
            "note": "",
            "created_at": datetime.now(),
        })
        
        response = client.get("/api/expenses/")
        
        data = response.get_json()
        expense = data["data"][0]
        
        assert "id" in expense
        assert "_id" not in expense
        assert isinstance(expense["id"], str)


class TestCategorySummaryEndpoint:
    """Test GET /api/expenses/summary endpoint."""

    def test_summary_empty(self, client):
        """Test summary when no expenses exist."""
        response = client.get("/api/expenses/summary")
        
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert data["data"] == []

    def test_summary_single_category(self, client, mock_mongo):
        """Test summary with single category."""
        db = mock_mongo["test_smart_expense_tracker"]
        db.expenses.insert_many([
            {"amount": 25.00, "category": "Food", "date": "2024-04-15", "note": "", "created_at": datetime.now()},
            {"amount": 15.00, "category": "Food", "date": "2024-04-14", "note": "", "created_at": datetime.now()},
        ])
        
        response = client.get("/api/expenses/summary")
        
        assert response.status_code == 200
        data = response.get_json()
        summary = data["data"]
        
        assert len(summary) == 1
        assert summary[0]["category"] == "Food"
        assert summary[0]["total"] == 40.00
        assert summary[0]["count"] == 2

    def test_summary_multiple_categories(self, client, mock_mongo):
        """Test summary with multiple categories."""
        db = mock_mongo["test_smart_expense_tracker"]
        db.expenses.insert_many([
            {"amount": 25.00, "category": "Food", "date": "2024-04-15", "note": "", "created_at": datetime.now()},
            {"amount": 50.00, "category": "Transport", "date": "2024-04-15", "note": "", "created_at": datetime.now()},
            {"amount": 100.00, "category": "Shopping", "date": "2024-04-14", "note": "", "created_at": datetime.now()},
        ])
        
        response = client.get("/api/expenses/summary")
        
        assert response.status_code == 200
        data = response.get_json()
        summary = data["data"]
        
        assert len(summary) == 3
        # Should be sorted by total descending
        assert summary[0]["total"] == 100.00  # Shopping
        assert summary[1]["total"] == 50.00   # Transport
        assert summary[2]["total"] == 25.00   # Food

    def test_summary_sorted_by_total(self, client, mock_mongo):
        """Test that summary is sorted by total amount descending."""
        db = mock_mongo["test_smart_expense_tracker"]
        db.expenses.insert_many([
            {"amount": 5.00, "category": "Food", "date": "2024-04-15", "note": "", "created_at": datetime.now()},
            {"amount": 200.00, "category": "Shopping", "date": "2024-04-15", "note": "", "created_at": datetime.now()},
            {"amount": 50.00, "category": "Transport", "date": "2024-04-15", "note": "", "created_at": datetime.now()},
            {"amount": 75.00, "category": "Entertainment", "date": "2024-04-15", "note": "", "created_at": datetime.now()},
        ])
        
        response = client.get("/api/expenses/summary")
        
        data = response.get_json()
        summary = data["data"]
        
        totals = [s["total"] for s in summary]
        assert totals == [200.00, 75.00, 50.00, 5.00]


class TestSpendingInsightsEndpoint:
    """Test GET /api/expenses/insights endpoint."""

    def test_insights_no_expenses(self, client):
        """Test insights when no expenses exist."""
        response = client.get("/api/expenses/insights")
        
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert len(data["insights"]) > 0
        assert "No expenses" in data["insights"][0]

    def test_insights_high_spending(self, client, mock_mongo):
        """Test that high spending triggers insight."""
        now = datetime.now()
        today_str = now.strftime("%Y-%m-%d")
        
        db = mock_mongo["test_smart_expense_tracker"]
        db.expenses.insert_many([
            {"amount": 400.00, "category": "Food", "date": today_str, "note": "", "created_at": now},
            {"amount": 300.00, "category": "Transport", "date": today_str, "note": "", "created_at": now},
            {"amount": 300.00, "category": "Shopping", "date": today_str, "note": "", "created_at": now},
        ])
        
        response = client.get("/api/expenses/insights")
        
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        insights_text = " ".join(data["insights"])
        # Should have warning about high spending
        assert any("Food" in ins or "spending" in ins for ins in data["insights"])

    def test_insights_balanced_spending(self, client, mock_mongo):
        """Test positive insight for balanced spending."""
        db = mock_mongo["test_smart_expense_tracker"]
        db.expenses.insert_many([
            {"amount": 25.00, "category": "Food", "date": "2024-04-15", "note": "", "created_at": datetime.now()},
            {"amount": 25.00, "category": "Transport", "date": "2024-04-15", "note": "", "created_at": datetime.now()},
            {"amount": 25.00, "category": "Shopping", "date": "2024-04-15", "note": "", "created_at": datetime.now()},
            {"amount": 25.00, "category": "Entertainment", "date": "2024-04-15", "note": "", "created_at": datetime.now()},
        ])
        
        response = client.get("/api/expenses/insights")
        
        data = response.get_json()
        assert any("Great job" in ins or "✅" in ins for ins in data["insights"])


class TestDeleteEndpoint:
    """Test DELETE /api/expenses/<id> endpoint."""

    def test_delete_expense_success(self, client, mock_mongo):
        """Test successfully deleting an expense."""
        from bson import ObjectId
        
        db = mock_mongo["test_smart_expense_tracker"]
        doc_id = ObjectId()
        db.expenses.insert_one({
            "_id": doc_id,
            "amount": 25.00,
            "category": "Food",
            "date": "2024-04-15",
            "note": "",
            "created_at": datetime.now(),
        })
        
        response = client.delete(f"/api/expenses/{str(doc_id)}")
        
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert data["data"]["amount"] == 25.00

    def test_delete_nonexistent_expense(self, client):
        """Test deleting non-existent expense returns 404."""
        from bson import ObjectId
        
        fake_id = str(ObjectId())
        response = client.delete(f"/api/expenses/{fake_id}")
        
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data

    def test_delete_invalid_id_format(self, client):
        """Test deleting with invalid ID format returns 404."""
        response = client.delete("/api/expenses/invalid-id")
        
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data


class TestHealthCheckEndpoint:
    """Test GET /api/health endpoint."""

    def test_health_check_success(self, client):
        """Test that health check returns ok status."""
        response = client.get("/api/health")
        
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "ok"
