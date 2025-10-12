import pytest
from unittest.mock import MagicMock
from models import Task
from services.task_service import TaskService


@pytest.fixture
def mock_repo():
    return MagicMock()


@pytest.fixture
def mock_user_repo():
    return MagicMock()


@pytest.fixture
def service(mock_repo, mock_user_repo):
    return TaskService(repository=mock_repo, user_repo=mock_user_repo)


def test_check_user_exists_returns_true_if_user_found(service, mock_user_repo):
    mock_user_repo.get_user_by_id_db.return_value = "user"
    assert service._check_user_exists(1) is True


def test_check_user_exists_returns_false_if_no_user(service, mock_user_repo):
    mock_user_repo.get_user_by_id_db.return_value = None
    assert service._check_user_exists(1) is False


def test_create_task_calls_user_check(service, mock_user_repo):
    mock_user_repo.get_user_by_id_db.return_value = "user"
    service.create_task("Task1", 1, "2025-10-12")
    mock_user_repo.get_user_by_id_db.assert_called_once_with(1)


def test_create_task_raises_error_if_user_not_found(service, mock_user_repo):
    mock_user_repo.get_user_by_id_db.return_value = None
    with pytest.raises(ValueError, match="User with id=1 does not exist."):
        service.create_task("Task1", 1, "2025-10-12")


def test_create_task_calls_repo_create_task_db(service, mock_repo, mock_user_repo):
    mock_user_repo.get_user_by_id_db.return_value = "user"
    service.create_task("T", 1, "2025-10-12")
    mock_repo.create_task_db.assert_called_once()


def test_create_task_returns_repository_result(service, mock_repo, mock_user_repo):
    mock_user_repo.get_user_by_id_db.return_value = "user"
    mock_repo.create_task_db.return_value = "task"
    result = service.create_task("T", 1, "2025-10-12")
    assert result == "task"


def test_get_tasks_for_user_checks_user(service, mock_user_repo):
    mock_user_repo.get_user_by_id_db.return_value = "user"
    service.get_tasks_for_user(2)
    mock_user_repo.get_user_by_id_db.assert_called_once_with(2)


def test_get_tasks_for_user_raises_if_user_not_found(service, mock_user_repo):
    mock_user_repo.get_user_by_id_db.return_value = None
    with pytest.raises(ValueError, match="User with id=2 does not exist."):
        service.get_tasks_for_user(2)


def test_get_tasks_for_user_returns_result(service, mock_repo, mock_user_repo):
    mock_user_repo.get_user_by_id_db.return_value = "user"
    mock_repo.get_all_tasks_db.return_value = ["t1", "t2"]
    result = service.get_tasks_for_user(3)
    assert result == ["t1", "t2"]


def test_get_task_by_id_returns_task(service, mock_repo):
    mock_repo.get_task_by_id_db.return_value = "task"
    result = service.get_task_by_id(1)
    assert result == "task"


def test_get_task_by_id_raises_if_not_found(service, mock_repo):
    mock_repo.get_task_by_id_db.return_value = None
    with pytest.raises(ValueError, match="Task with id=9 does not exist."):
        service.get_task_by_id(9)


def test_update_task_calls_get_task_by_id(service, mock_repo):
    mock_repo.get_task_by_id_db.return_value = Task(task_name="x", user_id=1)
    updated = Task(task_name="y", user_id=1)
    service.update_task(3, updated)
    mock_repo.get_task_by_id_db.assert_called_once_with(3)


def test_update_task_sets_task_id(service, mock_repo):
    mock_repo.get_task_by_id_db.return_value = Task(task_name="x", user_id=1)
    updated = Task(task_name="y", user_id=1)
    service.update_task(5, updated)
    assert updated.task_id == 5


def test_update_task_returns_repo_result(service, mock_repo):
    mock_repo.get_task_by_id_db.return_value = Task(task_name="x", user_id=1)
    mock_repo.update_user_db.return_value = "updated"
    updated = Task(task_name="y", user_id=1)
    result = service.update_task(5, updated)
    assert result == "updated"


def test_update_task_raises_if_not_found(service, mock_repo):
    mock_repo.get_task_by_id_db.return_value = None
    with pytest.raises(ValueError, match="Task with id=4 does not exist."):
        service.update_task(4, Task(task_name="x", user_id=1))


def test_delete_task_checks_user(service, mock_user_repo, mock_repo):
    mock_user_repo.get_user_by_id_db.return_value = "user"
    mock_repo.get_task_by_id_db.return_value = Task(task_name="x", user_id=1)
    service.delete_task(1, 2)
    mock_user_repo.get_user_by_id_db.assert_called_once_with(2)


def test_delete_task_raises_if_user_not_found(service, mock_user_repo):
    mock_user_repo.get_user_by_id_db.return_value = None
    with pytest.raises(ValueError, match="User with id=2 does not exist."):
        service.delete_task(1, 2)


def test_delete_task_calls_delete_task_db(service, mock_repo, mock_user_repo):
    mock_user_repo.get_user_by_id_db.return_value = "user"
    task = Task(task_name="del", user_id=1)
    mock_repo.get_task_by_id_db.return_value = task
    service.delete_task(10, 1)
    mock_repo.delete_task_db.assert_called_once_with(task)


def test_delete_task_returns_result(service, mock_repo, mock_user_repo):
    mock_user_repo.get_user_by_id_db.return_value = "user"
    task = Task(task_name="del", user_id=1)
    mock_repo.get_task_by_id_db.return_value = task
    mock_repo.delete_task_db.return_value = "deleted"
    result = service.delete_task(10, 1)
    assert result == "deleted"


def test_delete_task_raises_if_task_not_found(service, mock_repo, mock_user_repo):
    mock_user_repo.get_user_by_id_db.return_value = "user"
    mock_repo.get_task_by_id_db.return_value = None
    with pytest.raises(ValueError, match="Task with id=10 does not exist."):
        service.delete_task(10, 1)
