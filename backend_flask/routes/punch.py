from flask import Blueprint, request, jsonify

punch_bp = Blueprint("punch", __name__)

@punch_bp.route("/", methods=["POST"])
def punch():
    data = request.form
    return jsonify({"msg": "Punch received", "data": data}), 200
