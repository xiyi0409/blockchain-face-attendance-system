from flask import Blueprint, request, jsonify
from ipfs.ipfs_upload import upload_to_ipfs
from blockchain.web3_connect import send_to_blockchain
from database.db import insert_record
import time

punch_bp = Blueprint("punch", __name__)

@punch_bp.route("/", methods=["POST"])
def punch():
    try:
        # 取得表單資料
        employee_id = request.form.get("employee_id")
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")

        if not employee_id:
            return jsonify({"error": "Missing employee_id"}), 400

        # 取得圖片
        if "image" not in request.files:
            return jsonify({"error": "Missing image file"}), 400

        image_file = request.files["image"]

        # Step 1: 上傳 IPFS
        cid = upload_to_ipfs(image_file)

        # Step 2: 產生 timestamp
        timestamp = int(time.time())

        # Step 3: 上鏈（智能合約 addRecord）
        tx_hash = send_to_blockchain(cid, employee_id)

        # Step 4: 寫入 SQLite
        insert_record(employee_id, timestamp, latitude, longitude, cid, tx_hash)

        # 回傳結果
        return jsonify({
            "status": "success",
            "employee_id": employee_id,
            "cid": cid,
            "tx_hash": tx_hash,
            "timestamp": timestamp
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

