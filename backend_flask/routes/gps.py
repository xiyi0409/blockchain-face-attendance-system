from flask import Blueprint, request, jsonify
from database.db import insert_gps_log
import time

gps_bp = Blueprint("gps", __name__)

@gps_bp.route("/", methods=["POST"])
def gps_log():
    try:
        employee_id = request.json.get("employee_id")
        lat = request.json.get("latitude")
        lng = request.json.get("longitude")
        timestamp = int(time.time())

        if not employee_id:
            return jsonify({"error": "Missing employee_id"}), 400

        insert_gps_log(employee_id, timestamp, lat, lng)

        return jsonify({
            "status": "ok",
            "employee_id": employee_id,
            "timestamp": timestamp
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
