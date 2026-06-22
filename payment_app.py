from flask import Flask
import psycopg2
import os

app = Flask(__name__)

def connect_db():
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST", "postgres-service"),
        port=os.environ.get("DB_PORT", "5432"),
        database=os.environ.get("DB_NAME", "payments"),
        user=os.environ.get("DB_USER", "admin"),
        password=os.environ.get("DB_PASSWORD", "secret")
    )
    return conn

connect_db()

@app.route("/")
def home():
    return "Payment service is running!"

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
