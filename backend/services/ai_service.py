import os
import json
import time
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import List, Dict

from utils.logger import get_logger

logger = get_logger(__name__)

# Thresholds (% of total spend) above which a warning insight is generated
CATEGORY_THRESHOLDS = {
    "Food": 0.35,
    "Shopping": 0.30,
    "Entertainment": 0.25,
    "Transport": 0.20,
}

WEEKLY_HIGH_SPEND_THRESHOLD = 200  # absolute $$$ value

# Simple Rate Limiter Memory
_last_llm_call_time = 0.0
_LLM_RATE_LIMIT_SECONDS = 60.0


def generate_insights(expenses: List[Dict]) -> List[str]:
    """
    Hybrid AI insight generator.
    First attempts to call an LLM (if configured). Fallbacks to deterministic rule-based insights.
    Returns a list of human-readable insight strings.
    """
    if not expenses:
        return ["No expenses recorded yet. Start adding expenses to get insights!"]

    # Try LLM first
    llm_insights = _try_generate_llm_insights(expenses)
    if llm_insights:
        return llm_insights
        
    logger.info("Falling back to rule-based insights")
    return _generate_rule_based_insights(expenses)


def _try_generate_llm_insights(expenses: List[Dict]) -> List[str]:
    """Mock/Skeleton function for external LLM call. Wrapped securely."""
    global _last_llm_call_time
    
    now = time.time()
    if now - _last_llm_call_time < _LLM_RATE_LIMIT_SECONDS:
        logger.info("LLM rate limit reached. Using fallback.")
        return []
        
    try:
        # We simulate checking for an API key to determine if LLM generation would happen
        if not os.getenv("LLM_API_KEY"):
            return []
            
        # Example of where LLM call would formally execute:
        # _last_llm_call_time = now
        # response = openai_client.chat.completions.create(...)
        # return json.loads(response.content).get("insights", [])
        
        return [] 
        
    except Exception as e:
        logger.error(f"LLM insight generation failed: {e}")
        return []


def _generate_rule_based_insights(expenses: List[Dict]) -> List[str]:
    """Deterministic rule-based insights fallback."""
    insights = []

    # 1. Category-wise percentage analysis
    category_totals: Dict[str, float] = defaultdict(float)
    total_spend = 0.0

    for expense in expenses:
        amt = float(expense.get("amount", 0))
        cat = expense.get("category", "Other")
        category_totals[cat] += amt
        total_spend += amt

    if total_spend > 0:
        for cat, spent in category_totals.items():
            pct = spent / total_spend
            threshold = CATEGORY_THRESHOLDS.get(cat, 0.40)
            if pct > threshold:
                insights.append(
                    f"⚠️ You're spending {pct:.0%} of your budget on {cat} "
                    f"(${spent:.2f}). Consider cutting back."
                )

    # 2. High weekly spending alert
    now = datetime.now(timezone.utc)
    week_ago = now - timedelta(days=7)
    weekly_total = 0.0
    weekly_by_category: Dict[str, float] = defaultdict(float)

    for expense in expenses:
        try:
            exp_date = datetime.fromisoformat(expense.get("date", "")).replace(
                tzinfo=timezone.utc
            )
        except (ValueError, TypeError):
            continue
        if exp_date >= week_ago:
            amt = float(expense.get("amount", 0))
            weekly_total += amt
            weekly_by_category[expense.get("category", "Other")] += amt

    if weekly_total > WEEKLY_HIGH_SPEND_THRESHOLD:
        insights.append(
            f"📈 You've spent ${weekly_total:.2f} in the last 7 days — "
            f"that's above your weekly target of ${WEEKLY_HIGH_SPEND_THRESHOLD}."
        )

    if weekly_by_category:
        top_cat = max(weekly_by_category, key=weekly_by_category.get)
        insights.append(
            f"🍽️ Your top spending category this week is {top_cat} "
            f"(${weekly_by_category[top_cat]:.2f})."
        )

    # 3. Positive reinforcement
    if not insights:
        insights.append(
            "✅ Great job! Your spending looks well-balanced across all categories."
        )

    return insights
