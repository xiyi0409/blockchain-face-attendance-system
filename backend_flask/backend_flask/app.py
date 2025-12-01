from flask import Flask
from routes.punch import punch_bp
from routes.gps import gps_bp
from routes.records import records_bp
from routes.employees import employees_bp

app = Flask(__name__)

@app.route("/")
def home():
    return "Blockchain Attendance System Backend Running"

app.register_blueprint(punch_bp, url_prefix="/punch")
app.register_blueprint(gps_bp, url_prefix="/gps")
app.register_blueprint(records_bp, url_prefix="/records")
app.register_blueprint(employees_bp, url_prefix="/employees")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
