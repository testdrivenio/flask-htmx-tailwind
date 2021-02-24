from flask import Flask, render_template, request
from flask_assets import Bundle, Environment

from todo import todos

app = Flask(__name__)

css = Bundle("src/main.css", output="dist/main.css", filters="postcss")
assets = Environment(app)
assets.register("css", css)
css.build()


@app.route("/")
def homepage():
    return render_template("index.html", todos=[])


@app.route("/search", methods=["POST"])
def search_todo():
    search_term = request.form.get("search")
    if len(search_term) == 0:
        return render_template("todo.html", todos=[])
    res_todos = []
    for todo in todos:
        if search_term in todo["title"]:
            res_todos.append(todo)
    return render_template("todo.html", todos=res_todos)


if __name__ == "__main__":
    app.run(debug=True)