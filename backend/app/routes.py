from flask import Blueprint, jsonify, request
from .db import ping_database, name
import logging

api_bp = Blueprint("api", __name__)

# Configure a logger for error reporting
logger = logging.getLogger(__name__)

@api_bp.get("/health")
def api_health():
    """Lightweight health endpoint for API layer monitoring."""
    return jsonify({"status": "ok", "service": "api"})

@api_bp.get("/db/ping")
def db_ping():
    """Verifies DB connectivity/credentials with a trivial SELECT."""
    ok, error = ping_database()
    if not ok and error:
        # Log the detailed error internally, avoid exposing sensitive info to client
        logger.error("DB ping failed: %s", error)
    return jsonify({
        "status": "ok" if ok else "error",
        "error": None if ok else "Database connection failed",
    })

# Example insert route (commented):
# from flask import request
# from .db import insert_name
#
# @api_bp.post("/names")
# def create_name():
#     """Minimal insert endpoint; expects JSON body { "name": "...", "email": "..." }."""
#     data = request.get_json(silent=True) or {}
#     name = (data.get("name") or "").strip()
#     email = (data.get("email") or "").strip()
#     if not name or not email:
#         return jsonify({"status": "error", "error": "name and email are required"}), 400
#
#     ok, error = insert_name(name)
#     if not ok:
#         return jsonify({"status": "error", "error": error}), 500
#     return jsonify({"status": "ok"})

@api_bp.post("/names")
def create_name():
    data = request.get_json(silent=True) or {}
    person_name = (data.get("name") or "").strip()
    if not person_name:
        return jsonify({"status": "error", "error": "name needed"}), 400
    ok, error = name(person_name)
    if not ok:
        return jsonify({"status": "error", "error": error or "insert failed"}),500
    return jsonify({"status": "ok"})