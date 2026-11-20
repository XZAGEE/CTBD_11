
from flask import Flask
import redis
import os
import time

app = Flask(__name__)

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=6379,
    decode_responses=True
)

@app.route("/")
def index():
    visits = redis_client.incr("visits")

    return f"""
    <h1>Docker Compose Lab 11</h1>
    <h2>Application is running!</h2>
    <p>Number of visits: {visits}</p>
    <p>Connected to Redis successfully!</p>
    """

@app.route("/health")
def health():
    try:
        redis_client.ping()
        return {"status": "healthy", "redis": "connected"}, 200
    except redis.RedisError:
        return {"status": "unhealthy", "redis": "disconnected"}, 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
