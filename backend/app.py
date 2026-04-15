import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from routes.expense_routes import expense_bp
from utils.error_handlers import register_error_handlers

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False
    CORS(app, origins="*")

    @app.get("/api/health")
    def health_check():
        return jsonify({"status": "ok"}), 200

    # Register blueprints
    app.register_blueprint(expense_bp, url_prefix="/api/expenses")

    # Register error handlers
    register_error_handlers(app)

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("FLASK_PORT", 5000))
    app.run(debug=True, port=port)
