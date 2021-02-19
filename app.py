import json
import time
from flask import Flask, render_template, request
from flask_sockets import Sockets

app = Flask(__name__)
sockets = Sockets(app)

todos = [
    {"id": 1, "title": "walk the dog", "completed": False},
    {"id": 2, "title": "feed the cat", "completed": False},
]


@sockets.route("/websocket")
def echo_socket(ws):
    while not ws.closed:
        message = ws.receive()
        message = json.loads(message)
        message = message.get("chat_message")
        ws.send(f"Received message: {message}")


@app.route("/")
def homepage():
    return render_template("index.html", todos=todos)


@app.route("/todo", methods=["POST"])
def add_todo():
    todo = request.form.get("todo")
    todos.append({"id": len(todos) + 1, "title": todo, "completed": False})
    return render_template("ajax.html", todos=todos)


@app.route("/polling")
def polling():
    return time.ctime()


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(("", 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()