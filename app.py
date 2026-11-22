
import os
import socket

import redis
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
CLUSTER_NAME = os.getenv("CLUSTER_NAME", "local-docker")
COUNTER_KEY = "visitor_count"

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
    socket_connect_timeout=2,
    socket_timeout=2,
)

PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Visitor Counter</title>
    <style>
        * { box-sizing: border-box; }
        body {
            margin: 0; min-height: 100vh; display: flex; align-items: center;
            justify-content: center; font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #1e3c72, #2a5298);
        }
        .card {
            background: #fff; padding: 40px 50px; border-radius: 16px;
            text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,.3);
            min-width: 340px;
        }
        h1 { margin: 0 0 10px; color: #1e3c72; font-size: 26px; }
        .count { font-size: 72px; font-weight: bold; color: #2a5298; margin: 10px 0; }
        .label { color: #666; font-size: 16px; }
        .info {
            margin-top: 25px; padding-top: 15px; border-top: 1px solid #eee;
            font-size: 13px; color: #888; text-align: left;
        }
        .info b { color: #444; }
        .error { color: #c0392b; font-size: 18px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="card">
        <h1>Visitor Counter</h1>
        {% if error %}
            <div class="error">Cannot reach Redis.<br>Count unavailable.</div>
        {% else %}
            <div class="count">{{ count }}</div>
            <div class="label">total visits</div>
        {% endif %}
        <div class="info">
            <div><b>Served by:</b> {{ hostname }}</div>
            <div><b>Cluster:</b> {{ cluster }}</div>
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    hostname = socket.gethostname()
    try:
        count = r.incr(COUNTER_KEY)
        return render_template_string(
            PAGE, count=count, error=False, hostname=hostname, cluster=CLUSTER_NAME
        )
    except redis.exceptions.RedisError:
        return (
            render_template_string(
                PAGE, count=0, error=True, hostname=hostname, cluster=CLUSTER_NAME
            ),
            503,
        )

@app.route("/api/visits")
def visits():
    """Returns the current count without incrementing it."""
    try:
        return jsonify(
            visits=int(r.get(COUNTER_KEY) or 0),
            hostname=socket.gethostname()
        )
    except redis.exceptions.RedisError:
        return jsonify(error="redis unavailable"), 503

@app.route("/health")
def health():
    return jsonify(status="ok"), 200

@app.route("/ready")
def ready():
    try:
        r.ping()
        return jsonify(status="ready"), 200
    except redis.exceptions.RedisError:
        return jsonify(status="redis unavailable"), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
