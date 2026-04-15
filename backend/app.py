import os
import uuid
import time
import logging
from flask import Flask, jsonify, request, g
from flask_cors import CORS
from dotenv import load_dotenv

from routes.expense_routes import expense_bp
from utils.error_handlers import register_error_handlers
from utils.logger import get_logger

load_dotenv()

logger = get_logger(__name__)

def create_app():
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False
    CORS(app, origins="*")
    
    # Disable default werkzeug logger to avoid duplicate basic logs
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.ERROR)

    @app.before_request
    def before_request():
        g.request_id = str(uuid.uuid4())
        g.start_time = time.time()
        logger.info(f"Incoming Request: {request.method} {request.path}")

    @app.after_request
    def after_request(response):
        duration = time.time() - getattr(g, 'start_time', time.time())
        logger.info(
            f"Completed Request: {request.method} {request.path} | Status: {response.status_code} | Duration: {duration:.3f}s"
        )
        if hasattr(g, 'request_id'):
            response.headers['X-Request-ID'] = g.request_id
        return response

    @app.get("/api/health")
    def health_check():
        response_data = {"status": "ok"}
        if hasattr(g, 'request_id'):
            response_data["request_id"] = g.request_id
        return jsonify(response_data), 200

    # Register blueprints
    app.register_blueprint(expense_bp, url_prefix="/api/expenses")

    # Register error handlers
    register_error_handlers(app)

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("FLASK_PORT", 5000))
    app.run(debug=True, port=port)
