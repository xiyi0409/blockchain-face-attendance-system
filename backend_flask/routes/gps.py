from flask import Blueprint, request, jsonify

gps_bp = Blueprint("gps", __name__)

@gps_bp.route("/", methods=["POST"])
def upload_gps():
    data = request.json
    return jsonify({"msg": "GPS received", "data": data}), 200
