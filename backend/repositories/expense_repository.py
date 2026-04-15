from bson import ObjectId
from typing import Dict, List, Optional
from models.db import get_expenses_collection


class ExpenseRepository:
    """
    Repository layer for Expense records.
    Handles all direct MongoDB transactions and queries.
    """

    @classmethod
    def get_collection(cls):
        return get_expenses_collection()

    @classmethod
    def insert_one(cls, doc: Dict) -> str:
        """Insert a single expense document."""
        result = cls.get_collection().insert_one(doc)
        return str(result.inserted_id)

    @classmethod
    def find_all(cls) -> List[Dict]:
        """Fetch all expenses, sorted by date descending."""
        return list(
            cls.get_collection().find().sort([("date", -1), ("created_at", -1)])
        )

    @classmethod
    def aggregate_category_summary(cls) -> List[Dict]:
        """Aggregate total spending per category."""
        pipeline = [
            {
                "$group": {
                    "_id": "$category",
                    "total": {"$sum": "$amount"},
                    "count": {"$sum": 1},
                }
            },
            {"$sort": {"total": -1}},
            {
                "$project": {
                    "_id": 0,
                    "category": "$_id",
                    "total": 1,
                    "count": 1,
                }
            },
        ]
        results = list(cls.get_collection().aggregate(pipeline))
        for r in results:
            r["total"] = round(float(r["total"]), 2)
        return results

    @classmethod
    def delete_by_id(cls, oid: ObjectId) -> Optional[Dict]:
        """Delete an expense by its exact ObjectId."""
        return cls.get_collection().find_one_and_delete({"_id": oid})
