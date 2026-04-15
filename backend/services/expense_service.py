from bson import ObjectId
from datetime import datetime, timezone
from typing import Dict, List, Optional

from repositories.expense_repository import ExpenseRepository
from schemas.expense_schema import ExpenseCreateSchema
from utils.logger import get_logger

logger = get_logger(__name__)


def _serialize(doc: Dict) -> Dict:
    """Convert a MongoDB document to a JSON-serializable dict."""
    serialized = {**doc, "id": str(doc["_id"])}
    serialized.pop("_id", None)
    created_at = serialized.get("created_at")
    if isinstance(created_at, datetime):
        serialized["created_at"] = created_at.isoformat()
    return serialized


def create_expense(data: Dict) -> Dict:
    """Validate and insert a new expense document."""
    schema = ExpenseCreateSchema(**data)
    doc = schema.model_dump()
    doc["created_at"] = datetime.now(timezone.utc)
    
    inserted_id = ExpenseRepository.insert_one(doc)
    doc["_id"] = inserted_id
    
    logger.info(f"Expense created: id={inserted_id}, category={doc['category']}")
    return _serialize(doc)


def get_all_expenses() -> List[Dict]:
    """Return all expenses sorted by date descending."""
    expenses = ExpenseRepository.find_all()
    return [_serialize(e) for e in expenses]


def get_category_summary() -> List[Dict]:
    """Aggregate total spending grouped by category."""
    return ExpenseRepository.aggregate_category_summary()


def delete_expense(expense_id: str) -> Optional[Dict]:
    """Delete an expense by ID. Returns the deleted doc or None."""
    try:
        oid = ObjectId(expense_id)
    except Exception:
        return None
        
    doc = ExpenseRepository.delete_by_id(oid)
    if doc:
        logger.info(f"Expense deleted: id={expense_id}")
        return _serialize(doc)
    return None
