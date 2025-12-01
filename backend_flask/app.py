from flask import Flask
from routes.punch import punch_bp
from routes.gps import gps_bp
from routes.records import records_bp
from routes.employees import employees_bp
from database.db import init_db

app = Flask(__name__)

# 初始化資料庫
init_db()

# API 路由註冊
app.register_blueprint(punch_bp, url_prefix="/punch")
app.register_blueprint(gps_bp, url_prefix="/gps")
app.register_blueprint(records_bp, url_prefix="/records")
app.register_blueprint(employees_bp, url_prefix="/employees")

@app.route("/")
def home():
    return {"message": "Backend is running."}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
