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

def _get_current_date():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")

class ExpenseCreateSchema(BaseModel):
    amount: float = Field(..., gt=0, description="Amount must be greater than 0")
    category: str = Field(..., min_length=1, description="Category is required")
    date: str = Field(default_factory=_get_current_date, description="ISO date string")
    note: str = Field(default="", max_length=500)

    @field_validator("category")
    @classmethod
    def validate_category(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Category cannot be empty")
        if v not in VALID_CATEGORIES:
            raise ValueError(
                f"Category must be one of: {', '.join(VALID_CATEGORIES)}"
            )
        return v

    @field_validator("date", mode="before")
    @classmethod
    def process_and_validate_date(cls, v):
        if not v:
            return _get_current_date()
        v_str = str(v).strip()
        
        if len(v_str) != 10:
            raise ValueError("Date must be exactly in YYYY-MM-DD format")
        
        try:
            parsed_date = datetime.strptime(v_str, "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError("Date must be in YYYY-MM-DD format") from exc
        
        # Prevent future dates
        now = datetime.now(timezone.utc)
        if parsed_date.date() > now.date():
            raise ValueError("Date cannot be in the future")
            
        return v_str

    @field_validator("note", mode="before")
    @classmethod
    def normalize_note(cls, v):
        if v is None:
            return ""
        return str(v).strip()


class ExpenseResponseSchema(BaseModel):
    id: str
    amount: float
    category: str
    date: str
    note: str

    model_config = {"from_attributes": True}
