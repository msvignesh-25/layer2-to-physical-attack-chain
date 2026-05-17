from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

LOG_FILE = "/home/kali/Documents/arp_project/arp_alerts.log"
CREDS_FILE = "/home/kali/Documents/arp_project/credentials.log"

def read_log(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r") as f:
        lines = f.readlines()
    return [line.strip() for line in lines if line.strip()]

@app.route("/")
def index():
    alerts = read_log(LOG_FILE)[-50:]
    creds = read_log(CREDS_FILE)[-20:]
    return render_template("index.html",alerts=alerts,creds=creds)

@app.route("/api/alerts")
def alerts():
    lines = read_log(LOG_FILE)
    return jsonify(lines[-50:])  # Last 50 alerts

@app.route("/api/credentials")
def credentials():
    lines = read_log(CREDS_FILE)
    return jsonify(lines[-20:])  # Last 20 captures

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
