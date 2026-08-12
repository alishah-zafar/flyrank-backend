from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN DEFAULT 0
        )
    """)
    # Insert 3 example tasks only if table is empty
    count = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    if count == 0:
        conn.execute("INSERT INTO tasks (title) VALUES ('Buy groceries')")
        conn.execute("INSERT INTO tasks (title) VALUES ('Learn Flask')")
        conn.execute("INSERT INTO tasks (title) VALUES ('Build an API')")
        conn.commit()
    conn.close()

init_db()

@app.route("/tasks")
def get_tasks():
    conn = get_db()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return jsonify([dict(task) for task in tasks])

if __name__ == "__main__":
    app.run(debug=True, port=5000)