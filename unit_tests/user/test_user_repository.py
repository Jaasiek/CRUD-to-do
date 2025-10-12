import pytest
from unittest.mock import MagicMock
from models import User
from repository.user_repository import UserRepository


@pytest.fixture
def mock_session():
    return MagicMock()


@pytest.fixture
def repo(mock_session):
    return UserRepository(session=mock_session)


def test_create_user_db_adds_user(repo, mock_session):
    user = User(username="test", role="admin")
    repo.create_user_db(user)
    mock_session.add.assert_called_once_with(user)


def test_create_user_db_commits(repo, mock_session):
    user = User(username="test", role="admin")
    repo.create_user_db(user)
    mock_session.commit.assert_called_once()


def test_create_user_db_returns_user(repo, mock_session):
    user = User(username="test", role="admin")
    result = repo.create_user_db(user)
    assert result == user


def test_update_user_db_merges_user(repo, mock_session):
    user = User(username="old", role="user")
    repo.update_user_db(user)
    mock_session.merge.assert_called_once_with(user)


def test_update_user_db_commits(repo, mock_session):
    user = User(username="old", role="user")
    repo.update_user_db(user)
    mock_session.commit.assert_called()


def test_get_user_by_id_db_queries_user(repo, mock_session):
    repo.get_user_by_id_db(1)
    mock_session.query.assert_called_once_with(User)


def test_get_user_by_id_db_filters_by_id(repo, mock_session):
    query_mock = mock_session.query.return_value
    repo.get_user_by_id_db(5)
    query_mock.filter_by.assert_called_once_with(id=5)


def test_get_user_by_id_db_returns_first_result(repo, mock_session):
    query_mock = mock_session.query.return_value
    query_mock.filter_by.return_value.first.return_value = "user_obj"
    result = repo.get_user_by_id_db(5)
    assert result == "user_obj"


def test_delete_user_db_deletes_user(repo, mock_session):
    user = User(username="to_delete", role="guest")
    repo.delete_user_db(user)
    mock_session.delete.assert_called_once_with(user)


def test_delete_user_db_commits(repo, mock_session):
    user = User(username="to_delete", role="guest")
    repo.delete_user_db(user)
    mock_session.commit.assert_called_once()
