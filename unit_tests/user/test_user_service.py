import pytest
from unittest.mock import MagicMock
from models import User
from services.user_service import UserService


@pytest.fixture
def mock_repository():
    return MagicMock()


@pytest.fixture
def service(mock_repository):
    return UserService(repository=mock_repository)


def test_create_user_calls_repository_create_user_db(service, mock_repository):
    service.create_user("john", "admin")
    mock_repository.create_user_db.assert_called_once()


def test_create_user_passes_user_object(service, mock_repository):
    service.create_user("john", "admin")
    created_user = mock_repository.create_user_db.call_args[0][0]
    assert isinstance(created_user, User)


def test_create_user_returns_repository_result(service, mock_repository):
    mock_repository.create_user_db.return_value = "user_obj"
    result = service.create_user("john", "admin")
    assert result == "user_obj"


def test_get_user_returns_existing_user(service, mock_repository):
    user = User(username="alice", role="user")
    mock_repository.get_user_by_id.return_value = user
    result = service.get_user(1)
    assert result == user


def test_get_user_calls_repository(service, mock_repository):
    mock_repository.get_user_by_id.return_value = User(username="a", role="b")
    service.get_user(2)
    mock_repository.get_user_by_id.assert_called_once_with(2)


def test_get_user_raises_error_if_not_found(service, mock_repository):
    mock_repository.get_user_by_id.return_value = None
    with pytest.raises(ValueError, match="User with id=5 does not exist."):
        service.get_user(5)


def test_update_user_calls_repository_get_user(service, mock_repository):
    mock_repository.get_user_by_id.return_value = User(username="x", role="y")
    updated_user = User(username="a", role="b")
    service.update_user(3, updated_user)
    mock_repository.get_user_by_id.assert_called_once_with(3)


def test_update_user_sets_updated_user_id(service, mock_repository):
    mock_repository.get_user_by_id.return_value = User(username="old", role="user")
    updated_user = User(username="new", role="admin")
    service.update_user(10, updated_user)
    assert updated_user.id == 10


def test_update_user_calls_update_user_db(service, mock_repository):
    mock_repository.get_user_by_id.return_value = User(username="old", role="user")
    updated_user = User(username="new", role="admin")
    service.update_user(10, updated_user)
    mock_repository.update_user_db.assert_called_once_with(updated_user)


def test_update_user_returns_result_from_repo(service, mock_repository):
    mock_repository.get_user_by_id.return_value = User(username="old", role="user")
    mock_repository.update_user_db.return_value = "updated"
    updated_user = User(username="new", role="admin")
    result = service.update_user(10, updated_user)
    assert result == "updated"


def test_update_user_raises_error_if_user_not_found(service, mock_repository):
    mock_repository.get_user_by_id.return_value = None
    updated_user = User(username="x", role="y")
    with pytest.raises(ValueError, match="User with id=9 does not exist."):
        service.update_user(9, updated_user)


def test_delete_user_calls_repository_get_user(service, mock_repository):
    mock_repository.get_user_by_id.return_value = User(username="x", role="y")
    service.delete_user(1)
    mock_repository.get_user_by_id.assert_called_once_with(1)


def test_delete_user_calls_delete_user_db(service, mock_repository):
    user = User(username="to_delete", role="guest")
    mock_repository.get_user_by_id.return_value = user
    service.delete_user(1)
    mock_repository.delete_user_db.assert_called_once_with(user)


def test_delete_user_returns_repository_result(service, mock_repository):
    mock_repository.get_user_by_id.return_value = User(username="x", role="y")
    mock_repository.delete_user_db.return_value = "deleted"
    result = service.delete_user(2)
    assert result == "deleted"


def test_delete_user_raises_error_if_not_found(service, mock_repository):
    mock_repository.get_user_by_id.return_value = None
    with pytest.raises(ValueError, match="User with id=7 does not exist."):
        service.delete_user(7)
