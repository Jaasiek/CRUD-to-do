from models import Task


class TaskService:
    def __init__(self, repository, user_repo) -> None:
        self.repository = repository
        self.user_repo = user_repo

    def _check_user_exists(self, user_id: int) -> bool:
        user = self.user_repo.get_user_by_id_db(user_id)
        return user is not None

    def create_task(self, name, user_id, due_date=None, priority="medium"):
        if not self._check_user_exists(user_id):
            raise ValueError(f"User with id={user_id} does not exist.")

        task = Task(task_name=name, user_id=user_id, due_date=due_date, priority=priority)
        return self.repository.create_task_db(task)

    def get_tasks_for_user(self, user_id):
        if not self._check_user_exists(user_id):
            raise ValueError(f"User with id={user_id} does not exist.")

        return self.repository.get_all_tasks_db(user_id)

    def update_task_status(self, task_id, user_id, status):
        if not self._check_user_exists(user_id):
            raise ValueError(f"User with id={user_id} does not exist.")

        task = self.repository.get_task_by_id_db(task_id, user_id)
        if not task:
            return None
        task.status = status
        return self.repository.update_task_db(task)

    def delete_task(self, task_id, user_id) -> bool:
        if not self._check_user_exists(user_id):
            raise ValueError(f"User with id={user_id} does not exist.")

        task = self.repository.get_task_by_id_db(task_id, user_id)
        if not task:
            raise ValueError(f"Task with id={task_id} does not exist.")
        return self.repository.delete_task_db(task)

