from models import User


class UserService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def create_user(self, username, role, created_at):
        user = User(username=username, role=role, created_at=created_at)
        return self.repository.create_user(user)

    def update_user(self, user_id, updated_user: User):
        user = self.repository.get_user_by_id(user_id)
        if not user:
            return None

        updated_user.id = user_id
        return self.repository.update_user(updated_user)

    def delete_user(self, user_id) -> bool:
        user = self.repository.get_user_by_id(user_id)
        if user:
            self.repository.delete_user(user)
            return True
        return False
