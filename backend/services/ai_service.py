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
    try:
        llm_insights = _try_generate_llm_insights(expenses)
        if llm_insights:
            return llm_insights
    except Exception as e:
        logger.error("LLM Generation unexpected error: %s", e)
        
    logger.info("Falling back to rule-based insights")
    return _generate_rule_based_insights(expenses)


def _try_generate_llm_insights(expenses: List[Dict]) -> List[str]:
    """Actual LLM insight generation using Gemini API."""
    global _last_llm_call_time
    
    now = time.time()
    if now - _last_llm_call_time < _LLM_RATE_LIMIT_SECONDS:
        logger.info("LLM rate limit reached. Using fallback.")
        return []
        
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return []
            
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        _last_llm_call_time = now
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        if not expenses:
            return []
            
        expenses_text = "\\n".join([f"- {e.get('date', 'Unknown')}: {e.get('category', 'Other')} ${e.get('amount', 0)}" for e in expenses])
        
        prompt = f"""
        You are a smart financial advisor. Here is a list of recent expenses.
        
        {expenses_text}
        
        Please provide exactly 3 short, insightful, and actionable financial tips or observations based on this spending data.
        Use emojis. Keep it concise (1 sentence per tip).
        Format your response as a JSON array of strings, like this:
        ["tip 1", "tip 2", "tip 3"]
        
        Only output the JSON array. Do not wrap it in markdown. Do not provide any other text.
        """
        
        response = model.generate_content(prompt)
        content = response.text.strip()
        
        if content.startswith("```"):
            content = "\\n".join(content.split("\\n")[1:-1])
            if content.endswith("```"):
                content = content[:-3]
            
        import json
        try:
            insights = json.loads(content)
            if isinstance(insights, list) and len(insights) > 0:
                return insights
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse LLM JSON output: {content}")
            
        return [] 
        
    except Exception as e:
        logger.error(f"LLM insight generation failed: {e}")
        return []


def _generate_rule_based_insights(expenses: List[Dict]) -> List[str]:
    """Deterministic rule-based insights fallback."""
    insights = []
    has_warning = False

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
                has_warning = True
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
        has_warning = True
        insights.append(
            f"📈 You've spent ${weekly_total:.2f} in the last 7 days — "
            f"that's above your weekly target of ${WEEKLY_HIGH_SPEND_THRESHOLD}."
        )

    if weekly_by_category and has_warning:
        top_cat = max(weekly_by_category, key=weekly_by_category.get)
        insights.append(
            f"🍽️ Your top spending category this week is {top_cat} "
            f"(${weekly_by_category[top_cat]:.2f})."
        )

    # 3. Positive reinforcement
    if not has_warning:
        insights.append(
            "✅ Great job! Your spending looks well-balanced across all categories."
        )

    return insights
