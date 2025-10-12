from models import User


class UserService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def create_user(self, username, role, created_at):
        user = User(username=username, role=role, created_at=created_at)
        return self.repository.create_user_db(user)

    def update_user(self, user_id, updated_user: User):
        user = self.repository.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"User with id={user_id} does not exist.")

        updated_user.id = user_id
        return self.repository.update_user_db(updated_user)

    def delete_user(self, user_id):
        user = self.repository.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"User with id={user_id} does not exist.")

        return self.repository.delete_user_db(user)
