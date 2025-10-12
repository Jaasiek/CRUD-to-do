from dataclasses import dataclass

from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models import Base
from services.task_service import TaskService
from repository.task_repository import TaskRepository
from repository.user_repository import UserRepository
from services.user_service import UserService


@dataclass
class Settings:
    DATABASE_URL: str


class AppFlask(Flask):
    def __init__(
            self,
            import_name,
            settings: Settings,
            static_url_path=None,
            static_folder="static",
            static_host=None,
            host_matching=False,
            subdomain_matching=False,
            template_folder="templates",
            instance_path=None,
            instance_relative_config=False,
            root_path=None,
    ) -> None:
        super().__init__(
            import_name,
            static_url_path,
            static_folder,
            static_host,
            host_matching,
            subdomain_matching,
            template_folder,
            instance_path,
            instance_relative_config,
            root_path,
        )

        self._settings = settings

    def run(self, *args, **kwargs) -> None:
        # database
        engine = create_engine(self._settings.DATABASE_URL)
        Base.metadata.create_all(engine)

        # session setup
        self._session = scoped_session(sessionmaker(engine))
        Base.query = self._session.query_property()

        # run method from base class
        super().run(*args, **kwargs)


settings = Settings(DATABASE_URL="postgresql://admin:admin@localhost:5434/po_db")

app = AppFlask(__name__, settings=settings)
task_repo = TaskRepository(app._session)
user_repo = UserRepository(app._session)
task_service = TaskService(task_repo, user_repo)
user_service = UserService(user_repo)


@app.post("/user")
def create_user():
    data = request.get_json()
    user = user_service.create_user(
        username=data['username'],
        role=data['role'],
    )
    return jsonify({"user_id": user.id, "success": True}), 201


@app.patch("/user/<int:user_id>")
def update_user(user_id):
    data = request.get_json()
    try:
        user = user_service.get_user(user_id)
        if user.username != data["username"]:
            user.username = data["username"]
        if user.role != data["role"]:
            user.role = data["role"]
        user_service.update_user(user_id, user)
        return jsonify({"success": True}), 202
    except ValueError as error:
        return jsonify({"error": error, "success": False}), 404


@app.delete("/user/<int:user_id>")
def delete_user(user_id):
    try:
        user_service.delete_user(user_id)
        return jsonify({"success": True}), 200
    except ValueError as error:
        return jsonify({"error": error, "success": False}), 404


@app.post("/tasks")
def create_task():
    data = request.get_json()
    try:
        task = task_service.create_task(
            name=data["task_name"],
            user_id=data["user_id"],
            status=data.get("status", "pending"),
            due_date=data["due_date"],
            priority=data.get("priority", "medium"),
        )
        return jsonify({"task_id": task.task_id, "task_name": task.task_name, "success": True}), 201
    except ValueError as error:
        return jsonify({"error": error, "success": False}), 400


@app.get("/tasks/<int:user_id>")
def get_all_tasks(user_id):
    try:
        tasks = task_service.get_tasks_for_user(user_id=user_id)
        for task in tasks:
            return jsonify({"task_id": task.task_id, "task_name": task.task_name, "task_status": task.status})
        return jsonify({"success": True}), 200
    except ValueError as error:
        return jsonify({"error": error, "success": False}), 400


@app.patch("/tasks/<int:task_id>")
def update_task(task_id):
    data = request.get_json()
    try:
        task = task_service.get_task_by_id(task_id)
        if task.task_name != data["task_name"]:
            task.task_name = data["task_name"]
        if task.user_id != data["user_id"]:
            task.user_id = data["user_id"]
        if task.status != data["status"]:
            task.status = data["status"]
        if task.due_date != data["due_date"]:
            task.due_date = data["due_date"]
        if task.priority != data["priority"]:
            task.priority = data["priority"]

        task_service.update_task(task_id, task)
        return jsonify({"success": True}), 202
    except ValueError as error:
        return jsonify({"error": error, "success": False}), 404


@app.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    user_id = request.args.get("user_id", type=int)
    try:
        task_service.delete_task(task_id, user_id)
        return jsonify({"success": True}), 202
    except ValueError as error:
        return jsonify({"error": error, "success": False}), 400


if __name__ == "__main__":
    app.run(debug=True, port=8080)
