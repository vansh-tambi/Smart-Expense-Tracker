from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field, field_validator


VALID_CATEGORIES = [
    "Food",
    "Transport",
    "Shopping",
    "Entertainment",
    "Health",
    "Utilities",
    "Education",
    "Other",
]


class ExpenseCreateSchema(BaseModel):
    amount: float = Field(..., gt=0, description="Amount must be greater than 0")
    category: str = Field(..., min_length=1, description="Category is required")
    date: Optional[str] = None  # ISO date string, defaults to today
    note: Optional[str] = ""

    @field_validator("category")
    @classmethod
    def validate_category(cls, v: str) -> str:
        if v not in VALID_CATEGORIES:
            raise ValueError(
                f"Category must be one of: {', '.join(VALID_CATEGORIES)}"
            )
        return v

    @field_validator("date", mode="before")
    @classmethod
    def set_default_date(cls, v):
        if v is None or v == "":
            return datetime.now(timezone.utc).strftime("%Y-%m-%d")
        return v


class ExpenseResponseSchema(BaseModel):
    id: str
    amount: float
    category: str
    date: str
    note: str

    model_config = {"from_attributes": True}
