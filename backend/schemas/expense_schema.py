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
        v = v.strip()
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
        return str(v).strip()

    @field_validator("date")
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError("Date must be in YYYY-MM-DD format") from exc
        return v

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
