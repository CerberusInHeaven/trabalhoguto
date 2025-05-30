from flask import Flask, jsonify
import os, psycopg2

DB_CFG = {
    "dbname": os.environ["POSTGRES_DB"],
    "user": os.environ["POSTGRES_USER"],
    "password": os.environ["POSTGRES_PASSWORD"],
    "host": os.environ["DB_HOST"], # resolverá para 'db'
    "port": 5432,
}

app = Flask(__name__)

def get_conn():
    return psycopg2.connect(**DB_CFG)

@app.route("/")
def root():
    return jsonify(message="world of warcraft mist of pandaria, 21 july")

@app.route("/visitantes")
def visitantes():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("CREATE TABLE IF NOT EXISTS visitas (n INT);")
            cur.execute("INSERT INTO visitas VALUES (1);")
            cur.execute("SELECT SUM(n) FROM visitas;")
            total, = cur.fetchone()
    return jsonify(total_visitas=total)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
