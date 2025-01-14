from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# INICIALIZAR O BANCO DE DADOS
def init_db():
    with sqlite3.connect("todo.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL
            )
        """)
        conn.commit()

# ROTA PRINCIPAL
@app.route("/")
def home():
    with sqlite3.connect("todo.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, description FROM tasks")
        todo_list = cursor.fetchall()
    return render_template("index.html", todo_list=todo_list)

# ADICIONAR UMA NOVA TAREFA
@app.route("/add", methods=["POST"])
def add_task():
    task = request.form.get("task")
    if task:
        with sqlite3.connect("todo.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (description) VALUES (?)", (task,))
            conn.commit()
    return redirect(url_for("home"))

# DELETAR UMA TAREFA
@app.route("/delete/<int:task_id>", methods=["GET"])
def delete_task(task_id):
    with sqlite3.connect("todo.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
    return redirect(url_for("home"))

# ATUALIZAR UMA TAREFA
@app.route("/update/<int:task_id>", methods=["GET", "POST"])
def update_page(task_id):
    with sqlite3.connect("todo.db") as conn:
        cursor = conn.cursor()
        if request.method == "POST":
            updated_task = request.form.get("updated_task")
            if updated_task:
                cursor.execute("UPDATE tasks SET description = ? WHERE id = ?", (updated_task, task_id))
                conn.commit()
            return redirect(url_for("home"))
        # GET: EXIBE O FORMULÁRIO COM A TAREFA ATUAL
        cursor.execute("SELECT description FROM tasks WHERE id = ?", (task_id,))
        task_to_update = cursor.fetchone()
    if task_to_update:
        return render_template("update_page.html", task_to_update=task_to_update[0], task_id=task_id)
    return redirect(url_for("home"))

if __name__ == "__main__":
    init_db()  # INICIALIZA O DB AO INICIAR O APLICATIVO
    app.run(debug=True)
