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

@app.route("/tasks/<int:id>")
def get_task(id):
    conn = get_db()
    task = conn.execute(
        "SELECT * FROM tasks WHERE id = ?", (id,)
    ).fetchone()
    conn.close()
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(dict(task))
@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400
    conn = get_db()
    conn.execute(
        "INSERT INTO tasks (title) VALUES (?)", 
        (data["title"],)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Task created"}), 201
@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    data = request.get_json()
    conn = get_db()
    conn.execute(
        "UPDATE tasks SET title=?, done=? WHERE id=?",
        (data.get("title"), data.get("done"), id)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Task updated"})

@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Task deleted"})
if __name__ == "__main__":
    app.run(debug=True, port=5000)