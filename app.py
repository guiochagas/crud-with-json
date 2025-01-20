from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.config["DATABASE"] = "todo.db"

def get_db_connection():
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL
            )
        """)

class TaskDAO: # (Data Access Object)
    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            return conn.execute("SELECT id, description FROM tasks").fetchall()

    @staticmethod
    def add(description):
        with get_db_connection() as conn:
            conn.execute("INSERT INTO tasks (description) VALUES (?)", (description,))
            conn.commit()

    @staticmethod
    def delete(task_id):
        with get_db_connection() as conn:
            conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()

    @staticmethod
    def update(task_id, description):
        with get_db_connection() as conn:
            conn.execute("UPDATE tasks SET description = ? WHERE id = ?", (description, task_id))
            conn.commit()

    @staticmethod
    def get(task_id):
        with get_db_connection() as conn:
            return conn.execute("SELECT description FROM tasks WHERE id = ?", (task_id,)).fetchone()

@app.before_request
def setup_db():
    init_db()

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        directory=app.static_folder,
        path='favicon.ico',
        mimetype='image/vnd.microsoft.icon' 
    )

@app.route("/")
def home():
    todo_list = TaskDAO.get_all()
    return render_template("index.html", todo_list=todo_list)

@app.route("/add", methods=["POST"])
def add_task():
    task = request.form.get("task")
    if task:
        TaskDAO.add(task)
    return redirect(url_for("home"))

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    TaskDAO.delete(task_id)
    return redirect(url_for("home"))

@app.route("/update/<int:task_id>", methods=["GET", "POST"])
def update_page(task_id):
    if request.method == "POST":
        updated_task = request.form.get("updated_task")
        if updated_task:
            TaskDAO.update(task_id, updated_task)
            return redirect(url_for("home"))
    task_to_update = TaskDAO.get(task_id)
    if task_to_update:
        return render_template("update_page.html", task_to_update=task_to_update["description"], task_id=task_id)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
