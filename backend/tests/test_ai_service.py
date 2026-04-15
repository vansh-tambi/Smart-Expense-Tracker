"""
Unit tests for AI insight service.
Tests rule-based expense analysis and insight generation.
"""
import pytest
from datetime import datetime, timedelta, timezone
from services.ai_service import generate_insights


class TestGenerateInsights:
    """Test AI insight generation."""

    def test_no_expenses_insight(self):
        """Test insight when no expenses exist."""
        insights = generate_insights([])
        
        assert len(insights) > 0
        assert "No expenses recorded yet" in insights[0]

    def test_empty_list_insight(self):
        """Test insight with empty list."""
        insights = generate_insights([])
        assert any("No expenses" in insight for insight in insights)

    def test_high_food_spending_insight(self):
        """Test warning when food spending exceeds threshold."""
        total = 1000.0
        expenses = [
            {"amount": 400.0, "category": "Food", "date": "2024-04-15"},  # 40% > 35% threshold
            {"amount": 300.0, "category": "Transport", "date": "2024-04-15"},
            {"amount": 300.0, "category": "Shopping", "date": "2024-04-15"},
        ]
        
        insights = generate_insights(expenses)
        
        assert any("Food" in insight and "⚠️" in insight for insight in insights)

    def test_high_shopping_spending_insight(self):
        """Test warning when shopping spending exceeds threshold."""
        expenses = [
            {"amount": 500.0, "category": "Shopping", "date": "2024-04-15"},  # >30%
            {"amount": 500.0, "category": "Food", "date": "2024-04-15"},
        ]
        
        insights = generate_insights(expenses)
        
        assert any("Shopping" in insight and "⚠️" in insight for insight in insights)

    def test_balanced_spending_insight(self):
        """Test positive insight when spending is balanced."""
        expenses = [
            {"amount": 35.0, "category": "Food", "date": "2024-04-15"},
            {"amount": 20.0, "category": "Transport", "date": "2024-04-15"},
            {"amount": 20.0, "category": "Shopping", "date": "2024-04-15"},
            {"amount": 25.0, "category": "Entertainment", "date": "2024-04-15"},
        ]
        
        insights = generate_insights(expenses)
        
        assert any("Great job" in insight and "✅" in insight for insight in insights)

    def test_high_weekly_spending_insight(self):
        """Test warning when weekly spending is high."""
        now = datetime.now(timezone.utc)
        today_str = now.strftime("%Y-%m-%d")
        
        expenses = [
            {"amount": 250.0, "category": "Food", "date": today_str},  # >$200 weekly threshold
            {"amount": 100.0, "category": "Transport", "date": today_str},
        ]
        
        insights = generate_insights(expenses)
        
        assert any("$350" in insight and "📈" in insight for insight in insights)

    def test_weekly_top_category_insight(self):
        """Test insight about top spending category this week."""
        now = datetime.now(timezone.utc)
        today_str = now.strftime("%Y-%m-%d")
        
        expenses = [
            {"amount": 150.0, "category": "Food", "date": today_str},
            {"amount": 50.0, "category": "Transport", "date": today_str},
        ]
        
        insights = generate_insights(expenses)
        
        assert any("Food" in insight and "top spending" in insight for insight in insights)

    def test_ignores_old_expenses_for_weekly_trend(self):
        """Test that expenses older than 7 days are ignored for weekly analysis."""
        now = datetime.now(timezone.utc)
        
        # Expense from 10 days ago (outside 7-day window)
        ten_days_ago = (now - timedelta(days=10)).strftime("%Y-%m-%d")
        
        expenses = [
            {"amount": 500.0, "category": "Food", "date": ten_days_ago},
        ]
        
        insights = generate_insights(expenses)
        
        # Should not trigger high weekly spending warning
        assert not any("📈" in insight and "7 days" in insight for insight in insights)

    def test_mixed_old_and_recent_expenses(self):
        """Test that only recent expenses count for weekly trend."""
        now = datetime.now(timezone.utc)
        today_str = now.strftime("%Y-%m-%d")
        
        # Expense from 10 days ago
        ten_days_ago = (now - timedelta(days=10)).strftime("%Y-%m-%d")
        
        expenses = [
            {"amount": 500.0, "category": "Food", "date": ten_days_ago},  # Ignored
            {"amount": 250.0, "category": "Transport", "date": today_str},  # Counted
        ]
        
        insights = generate_insights(expenses)
        
        # Should only count the $250, not the old $500
        assert not any("$750" in insight for insight in insights)

    def test_multiple_insights_generated(self):
        """Test that multiple insights can be generated for same data."""
        now = datetime.now(timezone.utc)
        today_str = now.strftime("%Y-%m-%d")
        
        expenses = [
            {"amount": 200.0, "category": "Food", "date": today_str},  # High food
            {"amount": 150.0, "category": "Transport", "date": today_str},
            {"amount": 100.0, "category": "Shopping", "date": today_str},
        ]
        
        insights = generate_insights(expenses)
        
        # Should have multiple insights (food warning + weekly trend + top category)
        assert len(insights) >= 2

    def test_handles_malformed_dates(self):
        """Test that service handles invalid date formats gracefully."""
        expenses = [
            {"amount": 25.0, "category": "Food", "date": "invalid-date"},
            {"amount": 30.0, "category": "Transport", "date": "2024-04-15"},
        ]
        
        # Should not crash
        insights = generate_insights(expenses)
        
        assert len(insights) > 0

    def test_handles_missing_fields(self):
        """Test that service handles missing fields gracefully."""
        expenses = [
            {"amount": 25.0},  # Missing category and date
            {"category": "Food", "date": "2024-04-15"},  # Missing amount
        ]
        
        # Should not crash
        insights = generate_insights(expenses)
        
        assert len(insights) > 0

    def test_entertainment_threshold(self):
        """Test entertainment spending threshold."""
        expenses = [
            {"amount": 300.0, "category": "Entertainment", "date": "2024-04-15"},  # >25%
            {"amount": 700.0, "category": "Food", "date": "2024-04-15"},
        ]
        
        insights = generate_insights(expenses)
        
        assert any("Entertainment" in insight and "⚠️" in insight for insight in insights)

    def test_health_category_no_threshold_alert(self):
        """Test that Health category (no specific threshold) uses default 40%."""
        expenses = [
            {"amount": 300.0, "category": "Health", "date": "2024-04-15"},  # 30% < 40% default
            {"amount": 700.0, "category": "Food", "date": "2024-04-15"},
        ]
        
        insights = generate_insights(expenses)
        
        # Should NOT have Health warning since 30% < 40%
        assert not any("Health" in insight and "⚠️" in insight for insight in insights)

    def test_high_health_spending(self):
        """Test Health spending warning when exceeds default threshold."""
        expenses = [
            {"amount": 450.0, "category": "Health", "date": "2024-04-15"},  # 45% > 40% default
            {"amount": 550.0, "category": "Food", "date": "2024-04-15"},
        ]
        
        insights = generate_insights(expenses)
        
        assert any("Health" in insight and "⚠️" in insight for insight in insights)

    def test_single_large_expense(self):
        """Test insight with a single large expense."""
        expenses = [
            {"amount": 500.0, "category": "Transport", "date": "2024-04-15"},
        ]
        
        insights = generate_insights(expenses)
        
        assert len(insights) > 0
        assert any("Transport" in insight for insight in insights)

    def test_many_small_expenses(self):
        """Test insight with many small expenses."""
        expenses = [
            {"amount": 1.0, "category": "Food", "date": "2024-04-15"}
            for _ in range(100)
        ]
        
        insights = generate_insights(expenses)
        
        assert len(insights) > 0

    def test_llm_generation_mocked(self, monkeypatch):
        """Test that LLM generation returns structured output when successful."""
        from services import ai_service
        monkeypatch.setenv("LLM_API_KEY", "fake_key")
        
        def mock_llm_call(prompt):
            return ["Mocked LLM Insight"]
            
        monkeypatch.setattr(ai_service, "_try_generate_llm_insights", mock_llm_call)
        ai_service._last_llm_call_time = 0
        
        expenses = [{"amount": 50, "category": "Food", "date": "2024-04-15"}]
        insights = generate_insights(expenses)
        
        assert len(insights) == 1
        assert insights[0] == "Mocked LLM Insight"

    def test_rate_limit_fallback(self, monkeypatch):
        """Test that rate limiting forces a fallback to rule-based insights."""
        from services import ai_service
        import time
        monkeypatch.setenv("LLM_API_KEY", "fake_key")
        
        ai_service._last_llm_call_time = time.time()
        
        expenses = [{"amount": 500, "category": "Food", "date": "2024-04-15"}]
        insights = generate_insights(expenses)
        
        assert any("⚠️ You're spending" in ins for ins in insights)

    def test_llm_failure_fallback(self, monkeypatch):
        """Test that LLM failure forces a fallback to rule-based insights."""
        from services import ai_service
        monkeypatch.setenv("LLM_API_KEY", "fake_key")
        
        def mock_llm_fail(prompt):
            raise Exception("LLM API Timeout")
            
        monkeypatch.setattr(ai_service, "_try_generate_llm_insights", mock_llm_fail)
        ai_service._last_llm_call_time = 0
        
        expenses = [{"amount": 500, "category": "Food", "date": "2024-04-15"}]
        insights = generate_insights(expenses)
        
        assert any("⚠️ You're spending" in ins for ins in insights)
