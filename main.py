from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

todo_list = []

@app.route("/")  # ROTA PRINCIPAL
def home():
    return render_template("index.html", todo_list=todo_list)


@app.route("/add", methods=["POST"])  # ADICIONAR UMA NOVA TAREFA
def add_task():
    task = request.form.get("task")
    if task:
        todo_list.append(task)
    return redirect(url_for("home"))


@app.route("/delete/<int:task_id>", methods=["GET"])  # DELETAR UMA TAREFA
def delete_task(task_id):
    if 0 <= task_id < len(todo_list):
        todo_list.pop(task_id)
    return redirect(url_for("home"))


@app.route("/update/<int:task_id>", methods=["GET", "POST"])  # ATUALIZAR UMA TAREFA
def update_page(task_id):
    if 0 <= task_id < len(todo_list):
        if request.method == "POST":
            updated_task = request.form.get("updated_task")
            if updated_task:
                todo_list[task_id] = updated_task
            return redirect(url_for("home"))
        # GET: Exibe o formulário com a tarefa atual
        task_to_update = todo_list[task_id]
        return render_template("update_page.html", task_to_update=task_to_update, task_id=task_id)


if __name__ == '__main__':
    app.run(debug=True)
