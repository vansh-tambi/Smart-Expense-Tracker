from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from services import expense_service, ai_service
from utils.logger import get_logger

logger = get_logger(__name__)

expense_bp = Blueprint("expenses", __name__)


@expense_bp.route("/", methods=["POST"])
def add_expense():
    """POST /api/expenses/ — Add a new expense."""
    payload = request.get_json(force=True) or {}
    expense = expense_service.create_expense(payload)
    return jsonify({"success": True, "data": expense}), 201


@expense_bp.route("/", methods=["GET"])
def list_expenses():
    """GET /api/expenses/ — Retrieve all expenses."""
    expenses = expense_service.get_all_expenses()
    return jsonify({"success": True, "data": expenses, "count": len(expenses)}), 200


@expense_bp.route("/summary", methods=["GET"])
def category_summary():
    """GET /api/expenses/summary — Category-wise spending totals."""
    summary = expense_service.get_category_summary()
    return jsonify({"success": True, "data": summary}), 200


@expense_bp.route("/insights", methods=["GET"])
def spending_insights():
    """GET /api/expenses/insights — AI-generated spending insights."""
    expenses = expense_service.get_all_expenses()
    insights = ai_service.generate_insights(expenses)
    return jsonify({"success": True, "insights": insights}), 200


@expense_bp.route("/<expense_id>", methods=["DELETE"])
def remove_expense(expense_id: str):
    """DELETE /api/expenses/<id> — Delete an expense."""
    deleted = expense_service.delete_expense(expense_id)
    if deleted is None:
        return jsonify({"error": "Expense not found"}), 404
    return jsonify({"success": True, "data": deleted}), 200
