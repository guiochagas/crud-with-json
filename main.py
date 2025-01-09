from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

todo_list = []

@app.route("/")
def home():
    return render_template("index.html", todo_list=todo_list)

@app.route("/add", methods=["POST"])
def add_task():
    task = request.form.get("task")
    if task:
        todo_list.append(task)
    return redirect(url_for("home"))

@app.route("/delete/<int:task_id>", methods=["GET"])
def delete_task(task_id):
    if 0 <= task_id < len(todo_list):
        todo_list.pop(task_id)
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)
