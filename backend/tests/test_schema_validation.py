"""
Unit tests for Pydantic schema validation.
Tests all validation rules for expenses.
"""
import pytest
from pydantic import ValidationError
from schemas.expense_schema import ExpenseCreateSchema, VALID_CATEGORIES
from datetime import datetime, timezone


class TestExpenseCreateSchema:
    """Test validation of ExpenseCreateSchema."""

    def test_valid_expense_minimal(self):
        """Test creating a valid expense with minimal fields."""
        data = {
            "amount": 25.50,
            "category": "Food",
        }
        expense = ExpenseCreateSchema(**data)
        assert expense.amount == 25.50
        assert expense.category == "Food"
        assert expense.note == ""
        # Default date should be today in YYYY-MM-DD format
        # It's set by field validator, so just verify it exists and is formatted correctly
        assert expense.date is not None
        import re
        assert re.match(r'^\d{4}-\d{2}-\d{2}$', expense.date)

    def test_valid_expense_full(self):
        """Test creating a valid expense with all fields."""
        data = {
            "amount": 100.00,
            "category": "Transport",
            "date": "2024-04-15",
            "note": "Monthly pass",
        }
        expense = ExpenseCreateSchema(**data)
        assert expense.amount == 100.00
        assert expense.category == "Transport"
        assert expense.date == "2024-04-15"
        assert expense.note == "Monthly pass"

    def test_amount_zero_fails(self):
        """Test that zero amount is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ExpenseCreateSchema(amount=0, category="Food")
        errors = exc_info.value.errors()
        assert len(errors) > 0
        assert "greater than 0" in str(errors[0])

    def test_amount_negative_fails(self):
        """Test that negative amount is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ExpenseCreateSchema(amount=-10.00, category="Food")
        errors = exc_info.value.errors()
        assert len(errors) > 0
        assert "greater than 0" in str(errors[0])

    def test_missing_amount_fails(self):
        """Test that missing amount is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ExpenseCreateSchema(category="Food")
        errors = exc_info.value.errors()
        assert len(errors) > 0
        assert "Field required" in str(errors)

    def test_missing_category_fails(self):
        """Test that missing category is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ExpenseCreateSchema(amount=25.00)
        errors = exc_info.value.errors()
        assert len(errors) > 0
        assert "Field required" in str(errors)

    def test_invalid_category_fails(self):
        """Test that invalid category is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ExpenseCreateSchema(amount=25.00, category="InvalidCategory")
        errors = exc_info.value.errors()
        assert len(errors) > 0
        assert "Category must be one of" in str(errors[0])

    def test_category_case_sensitive(self):
        """Test that category must match exact case."""
        # Lowercase should fail
        with pytest.raises(ValidationError):
            ExpenseCreateSchema(amount=25.00, category="food")

        # Uppercase should fail
        with pytest.raises(ValidationError):
            ExpenseCreateSchema(amount=25.00, category="FOOD")

    def test_category_whitespace_stripped(self):
        """Test that whitespace around category is trimmed."""
        expense = ExpenseCreateSchema(amount=25.00, category="  Food  ")
        assert expense.category == "Food"

    def test_all_valid_categories(self):
        """Test that all predefined categories are valid."""
        for cat in VALID_CATEGORIES:
            expense = ExpenseCreateSchema(amount=25.00, category=cat)
            assert expense.category == cat

    def test_invalid_date_format_fails(self):
        """Test that invalid date format is rejected."""
        invalid_dates = [
            "2024/04/15",
            "04-15-2024",
            "2024-4-15",
            "invalid",
        ]
        for date_str in invalid_dates:
            with pytest.raises(ValidationError) as exc_info:
                ExpenseCreateSchema(amount=25.00, category="Food", date=date_str)
            errors = exc_info.value.errors()
            assert len(errors) > 0

    def test_future_date_fails(self):
        """Test that future dates are rejected."""
        future_date = (datetime.now(timezone.utc) + __import__('datetime').timedelta(days=2)).strftime("%Y-%m-%d")
        with pytest.raises(ValidationError) as exc_info:
            ExpenseCreateSchema(amount=25.0, category="Food", date=future_date)
        assert "future" in str(exc_info.value)

    def test_valid_date_formats(self):
        """Test that valid ISO date format is accepted."""
        valid_dates = [
            "2024-04-15",
            "2024-01-01",
        ]
        for date_str in valid_dates:
            expense = ExpenseCreateSchema(
                amount=25.00, category="Food", date=date_str
            )
            assert expense.date == date_str

    def test_note_empty_string_default(self):
        """Test that note defaults to empty string."""
        expense = ExpenseCreateSchema(amount=25.00, category="Food")
        assert expense.note == ""

    def test_note_none_becomes_empty_string(self):
        """Test that None note is converted to empty string."""
        expense = ExpenseCreateSchema(
            amount=25.00, category="Food", note=None
        )
        assert expense.note == ""

    def test_note_whitespace_stripped(self):
        """Test that note whitespace is trimmed."""
        expense = ExpenseCreateSchema(
            amount=25.00, category="Food", note="  Some note  "
        )
        assert expense.note == "Some note"

    def test_amount_large_precision(self):
        """Test that large amounts with decimals work."""
        expense = ExpenseCreateSchema(
            amount=9999.99, category="Shopping"
        )
        assert expense.amount == 9999.99

    def test_amount_small_decimal(self):
        """Test that small decimal amounts work."""
        expense = ExpenseCreateSchema(
            amount=0.01, category="Food"
        )
        assert expense.amount == 0.01

    def test_date_none_defaults_to_today(self):
        """Test that None date defaults to today."""
        expense = ExpenseCreateSchema(amount=25.00, category="Food", date=None)
        from datetime import timezone
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        assert expense.date == today

    def test_date_empty_string_defaults_to_today(self):
        """Test that empty string date defaults to today."""
        expense = ExpenseCreateSchema(amount=25.00, category="Food", date="")
        from datetime import timezone
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        assert expense.date == today

