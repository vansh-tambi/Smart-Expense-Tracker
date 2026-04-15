from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from services import expense_service, ai_service
from utils.logger import get_logger

logger = get_logger(__name__)

expense_bp = Blueprint("expenses", __name__)


@expense_bp.route("/", methods=["POST"])
def add_expense():
    """POST /api/expenses/ — Add a new expense."""
    try:
        payload = request.get_json(force=True) or {}
        expense = expense_service.create_expense(payload)
        return jsonify({"success": True, "data": expense}), 201
    except ValidationError as e:
        errors = e.errors()
        logger.warning(f"Validation failed on add_expense: {errors}")
        return (
            jsonify(
                {
                    "error": "Validation failed",
                    "details": [
                        {
                            "field": ".".join(str(l) for l in err["loc"]),
                            "message": err["msg"],
                        }
                        for err in errors
                    ],
                }
            ),
            400,
        )
    except Exception as e:
        logger.error(f"Unexpected error on add_expense: {e}", exc_info=True)
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@expense_bp.route("/", methods=["GET"])
def list_expenses():
    """GET /api/expenses/ — Retrieve all expenses."""
    try:
        expenses = expense_service.get_all_expenses()
        return jsonify({"success": True, "data": expenses, "count": len(expenses)}), 200
    except Exception as e:
        logger.error(f"Unexpected error on list_expenses: {e}", exc_info=True)
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@expense_bp.route("/summary", methods=["GET"])
def category_summary():
    """GET /api/expenses/summary — Category-wise spending totals."""
    try:
        summary = expense_service.get_category_summary()
        return jsonify({"success": True, "data": summary}), 200
    except Exception as e:
        logger.error(f"Unexpected error on category_summary: {e}", exc_info=True)
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@expense_bp.route("/insights", methods=["GET"])
def spending_insights():
    """GET /api/expenses/insights — AI-generated spending insights."""
    try:
        expenses = expense_service.get_all_expenses()
        insights = ai_service.generate_insights(expenses)
        return jsonify({"success": True, "insights": insights}), 200
    except Exception as e:
        logger.error(f"Unexpected error on spending_insights: {e}", exc_info=True)
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@expense_bp.route("/<expense_id>", methods=["DELETE"])
def remove_expense(expense_id: str):
    """DELETE /api/expenses/<id> — Delete an expense."""
    try:
        deleted = expense_service.delete_expense(expense_id)
        if deleted is None:
            return jsonify({"error": "Expense not found"}), 404
        return jsonify({"success": True, "data": deleted}), 200
    except Exception as e:
        logger.error(f"Unexpected error on remove_expense: {e}", exc_info=True)
        return jsonify({"error": "Internal server error", "message": str(e)}), 500
