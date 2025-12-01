from flask import Blueprint, jsonify
from database.db import get_records

records_bp = Blueprint("records", __name__)

@records_bp.route("/", methods=["GET"])
def list_records():
    try:
        data = get_records()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
