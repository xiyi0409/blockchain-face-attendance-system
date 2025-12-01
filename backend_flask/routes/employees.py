from flask import Blueprint, request, jsonify
from database.db import insert_employee, get_employees

employees_bp = Blueprint("employees", __name__)

@employees_bp.route("/", methods=["POST"])
def add_employee():
    try:
        employee_id = request.json.get("employee_id")
        name = request.json.get("name")
        insert_employee(employee_id, name)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@employees_bp.route("/", methods=["GET"])
def list_employees():
    try:
        employees = get_employees()
        return jsonify(employees), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
