from flask import jsonify
from pydantic import ValidationError

from utils.logger import get_logger

logger = get_logger(__name__)


def register_error_handlers(app):

    @app.errorhandler(400)
    def bad_request(e):
        logger.warning(f"400 Bad Request: {e}")
        return jsonify({"error": "Bad request", "message": str(e)}), 400

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not found", "message": str(e)}), 404

    @app.errorhandler(500)
    def internal_error(e):
        logger.error(f"500 Internal Server Error: {e}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        errors = e.errors()
        logger.warning(f"Validation error: {errors}")
        return (
            jsonify(
                {
                    "error": "Validation failed",
                    "details": [
                        {"field": ".".join(str(l) for l in err["loc"]), "message": err["msg"]}
                        for err in errors
                    ],
                }
            ),
            400,
        )
