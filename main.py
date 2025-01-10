from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

todo_list = []

@app.route("/") # ROTA PRINCIPAL
def home():
    return render_template("index.html", todo_list=todo_list)


@app.route("/add", methods=["POST"]) # ADICIONAR UMA NOVA TAREFA
def add_task():
    task = request.form.get("task")
    if task:
        todo_list.append(task)
    return redirect(url_for("home"))


@app.route("/delete/<int:task_id>", methods=["GET"]) # DELETAR UMA TAREFA
def delete_task(task_id):
    if 0 <= task_id < len(todo_list):
        todo_list.pop(task_id)
    return redirect(url_for("home"))


@app.route("/update/<int:task_id>") # PÁGINA PARA ACESSAR A TAREFA À SER ATUALIZADA
def update_page(task_id):
    update_task = todo_list[task_id]
    return render_template("update_page.html", update_task=update_task)


@app.route("/new_task/<int:task_id>", methods=["GET"])
def new_task(task):
    if 0 <= task_id < len(todo_list):
        pass


if __name__ == '__main__':
    app.run(debug=True)
