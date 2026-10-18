
from flask import Flask, jsonify, request, send_from_directory
import json
import os

app = Flask(__name__, static_folder="frontend", static_url_path="")

FILE_NAME = "tasks.json"


def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_tasks(tasks):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4)


@app.route("/")
def home():
    return send_from_directory("frontend", "index.html")


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    return jsonify(load_tasks())


@app.route("/api/tasks", methods=["POST"])
def add_task():
    data = request.get_json(silent=True) or {}
    name = data.get("name", "").strip()

    if not name:
        return jsonify({"error": "Task name is required"}), 400

    tasks = load_tasks()
    task = {"name": name, "completed": False}
    tasks.append(task)
    save_tasks(tasks)

    return jsonify(task), 201


@app.route("/api/tasks/<int:index>", methods=["PATCH"])
def update_task(index):
    tasks = load_tasks()

    if index < 0 or index >= len(tasks):
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json(silent=True) or {}
    completed = data.get("completed")

    if not isinstance(completed, bool):
        return jsonify({"error": "A boolean completed value is required"}), 400

    tasks[index]["completed"] = completed
    save_tasks(tasks)

    return jsonify(tasks[index])


@app.route("/api/tasks/<int:index>", methods=["DELETE"])
def delete_task(index):
    tasks = load_tasks()

    if index < 0 or index >= len(tasks):
        return jsonify({"error": "Task not found"}), 404

    removed = tasks.pop(index)
    save_tasks(tasks)

    return jsonify({"message": "Task deleted", "task": removed})


if __name__ == "__main__":
    app.run(debug=True)
