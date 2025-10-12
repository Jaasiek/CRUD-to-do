from models import Task


class TaskRepository:
    def __init__(self, session) -> None:
        self.session = session

    def create_task(self, task: Task) -> Task:
        self.session.add(task)
        self.session.commit()
        return task

    def get_all_tasks(self, user_id: int):
        return self.session.query(Task).filter_by(user_id=user_id).all()

    def get_task_by_id(self, task_id: int, user_id: int):
        return self.session.query(Task).filter_by(task_id=task_id, user_id=user_id).first()

    def update_task(self, task: Task):
        self.session.query(Task).filter_by(task_id=task.task_id, user_id=task.user_id).update({"status": task.status})
        self.session.commit()

    def delete_task(self, task) -> None:
        self.session.delete(task)
        self.session.commit()
