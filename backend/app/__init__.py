import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv


def create_app() -> Flask:
    """Application factory creating the Flask app with minimal setup."""
    load_dotenv()

    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False

    # Restrict CORS in production; allow all in local dev
    frontend_origin = os.getenv("FRONTEND_ORIGIN", "*")
    CORS(app, resources={r"/*": {"origins": frontend_origin}})

    # Register API blueprint
    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.get("/")
    def root():
        return jsonify({"status": "ok"})

    return app
