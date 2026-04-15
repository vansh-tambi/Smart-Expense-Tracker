from flask import jsonify, g, has_request_context
from pydantic import ValidationError

from utils.logger import get_logger

logger = get_logger(__name__)


def build_error_response(message: str, status_code: int, details=None):
    response = {
        "error": message,
        "status": status_code,
    }
    if has_request_context() and hasattr(g, 'request_id'):
        response["request_id"] = g.request_id
        
    if details:
        response["details"] = details
        
    return jsonify(response), status_code


def register_error_handlers(app):

    @app.errorhandler(400)
    def bad_request(e):
        logger.warning(f"400 Bad Request: {e}")
        return build_error_response("Bad request", 400)

    @app.errorhandler(404)
    def not_found(e):
        logger.warning(f"404 Not Found: {e}")
        return build_error_response("Not found", 404)

    @app.errorhandler(500)
    def internal_error(e):
        logger.error(f"500 Internal Server Error: {e}", exc_info=True)
        return build_error_response("Internal server error", 500)

    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        errors = e.errors()
        logger.warning(f"Validation error: {errors}")
        details = [
            {"field": ".".join(str(l) for l in err["loc"]), "message": err["msg"]}
            for err in errors
        ]
        return build_error_response("Validation failed", 400, details=details)

    @app.errorhandler(Exception)
    def unhandled_exception(e):
        logger.error(f"Unhandled exception: {e}", exc_info=True)
        return build_error_response("Internal server error", 500)
