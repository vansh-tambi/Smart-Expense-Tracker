import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from routes.expense_routes import expense_bp
from utils.error_handlers import register_error_handlers

load_dotenv()


def create_app():
    app = Flask(__name__)
    CORS(app, origins="*")

    # Register blueprints
    app.register_blueprint(expense_bp, url_prefix="/api/expenses")

    # Register error handlers
    register_error_handlers(app)

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("FLASK_PORT", 5000))
    app.run(debug=True, port=port)
