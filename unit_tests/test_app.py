import pytest
from unittest.mock import MagicMock
from app import app


@pytest.fixture
def client(monkeypatch):
    mock_user_service = MagicMock()
    mock_task_service = MagicMock()

    monkeypatch.setattr("app.user_service", mock_user_service)
    monkeypatch.setattr("app.task_service", mock_task_service)

    app.testing = True
    with app.test_client() as client:
        yield client


def test_create_user_returns_201(client, monkeypatch):
    app.user_service.create_user.return_value.id = 1
    response = client.post("/user", json={"username": "john", "role": "admin"})
    assert response.status_code == 201


def test_create_user_response_contains_success(client):
    app.user_service.create_user.return_value.id = 2
    response = client.post("/user", json={"username": "mike", "role": "user"})
    assert response.get_json()["success"] is True


def test_update_user_returns_202(client):
    mock_user = MagicMock(username="old", role="user")
    app.user_service.get_user.return_value = mock_user
    response = client.patch("/user/1", json={"username": "new", "role": "admin"})
    assert response.status_code == 202


def test_update_user_returns_404_on_missing_user(client):
    app.user_service.get_user.side_effect = ValueError("not found")
    response = client.patch("/user/1", json={"username": "new", "role": "admin"})
    assert response.status_code == 404


def test_delete_user_returns_200(client):
    response = client.delete("/user/1")
    assert response.status_code == 200


def test_delete_user_returns_404_if_not_found(client):
    app.user_service.delete_user.side_effect = ValueError("not found")
    response = client.delete("/user/1")
    assert response.status_code == 404


def test_create_task_returns_201(client):
    task_mock = MagicMock(task_id=1, task_name="T1")
    app.task_service.create_task.return_value = task_mock
    response = client.post("/tasks", json={
        "task_name": "T1",
        "user_id": 1,
        "due_date": "2025-12-12"
    })
    assert response.status_code == 201


def test_create_task_returns_400_if_user_not_found(client):
    app.task_service.create_task.side_effect = ValueError("User with id=1 does not exist.")
    response = client.post("/tasks", json={
        "task_name": "T2",
        "user_id": 1,
        "due_date": "2025-12-12"
    })
    assert response.status_code == 400


def test_get_all_tasks_returns_200(client):
    app.task_service.get_tasks_for_user.return_value = []
    response = client.get("/tasks/1")
    assert response.status_code == 200


def test_get_all_tasks_returns_400_if_user_missing(client):
    app.task_service.get_tasks_for_user.side_effect = ValueError("User missing")
    response = client.get("/tasks/1")
    assert response.status_code == 400


def test_update_task_returns_202(client):
    mock_task = MagicMock(
        task_name="old", user_id=1, status="pending",
        due_date="2025-10-10", priority="medium"
    )
    app.task_service.get_task_by_id.return_value = mock_task
    response = client.patch("/tasks/1", json={
        "task_name": "new",
        "user_id": 1,
        "status": "done",
        "due_date": "2025-10-11",
        "priority": "high"
    })
    assert response.status_code == 202


def test_update_task_returns_404_if_not_found(client):
    app.task_service.get_task_by_id.side_effect = ValueError("not found")
    response = client.patch("/tasks/1", json={
        "task_name": "new",
        "user_id": 1,
        "status": "done",
        "due_date": "2025-10-11",
        "priority": "high"
    })
    assert response.status_code == 404


def test_delete_task_returns_202(client):
    response = client.delete("/tasks/1?user_id=1")
    assert response.status_code == 202


def test_delete_task_returns_400_if_user_missing(client):
    app.task_service.delete_task.side_effect = ValueError("User missing")
    response = client.delete("/tasks/1?user_id=1")
    assert response.status_code == 400
