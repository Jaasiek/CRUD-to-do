import pytest
from unittest.mock import MagicMock
from models import Task
from repository.task_repository import TaskRepository


@pytest.fixture
def mock_session():
    return MagicMock()


@pytest.fixture
def repo(mock_session):
    return TaskRepository(session=mock_session)


def test_create_task_db_adds_task(repo, mock_session):
    task = Task(task_name="Test", user_id=1)
    repo.create_task_db(task)
    mock_session.add.assert_called_once_with(task)


def test_create_task_db_commits(repo, mock_session):
    task = Task(task_name="Test", user_id=1)
    repo.create_task_db(task)
    mock_session.commit.assert_called_once()


def test_create_task_db_returns_task(repo, mock_session):
    task = Task(task_name="Test", user_id=1)
    result = repo.create_task_db(task)
    assert result == task


def test_get_all_tasks_db_queries_task(repo, mock_session):
    repo.get_all_tasks_db(1)
    mock_session.query.assert_called_once_with(Task)


def test_get_all_tasks_db_filters_by_user_id(repo, mock_session):
    query_mock = mock_session.query.return_value
    repo.get_all_tasks_db(2)
    query_mock.filter_by.assert_called_once_with(user_id=2)


def test_get_all_tasks_db_returns_all(repo, mock_session):
    query_mock = mock_session.query.return_value
    query_mock.filter_by.return_value.all.return_value = ["t1", "t2"]
    result = repo.get_all_tasks_db(3)
    assert result == ["t1", "t2"]


def test_get_task_by_id_db_queries_task(repo, mock_session):
    repo.get_task_by_id_db(1, 2)
    mock_session.query.assert_called_once_with(Task)


def test_get_task_by_id_db_filters_correctly(repo, mock_session):
    query_mock = mock_session.query.return_value
    repo.get_task_by_id_db(10, 20)
    query_mock.filter_by.assert_called_once_with(task_id=10, user_id=20)


def test_get_task_by_id_db_returns_first(repo, mock_session):
    query_mock = mock_session.query.return_value
    query_mock.filter_by.return_value.first.return_value = "task"
    result = repo.get_task_by_id_db(5, 1)
    assert result == "task"


def test_update_task_db_merges_task(repo, mock_session):
    task = Task(task_name="Update", user_id=1)
    repo.update_task_db(task)
    mock_session.merge.assert_called_once_with(task)


def test_update_task_db_commits(repo, mock_session):
    task = Task(task_name="Update", user_id=1)
    repo.update_task_db(task)
    mock_session.commit.assert_called()


def test_delete_task_db_deletes_task(repo, mock_session):
    task = Task(task_name="Delete", user_id=1)
    repo.delete_task_db(task)
    mock_session.delete.assert_called_once_with(task)


def test_delete_task_db_commits(repo, mock_session):
    task = Task(task_name="Delete", user_id=1)
    repo.delete_task_db(task)
    mock_session.commit.assert_called_once()
