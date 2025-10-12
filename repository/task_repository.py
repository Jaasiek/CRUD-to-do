from models import Task


class TaskRepository:
    def __init__(self, session) -> None:
        self.session = session

    def create_task_db(self, task: Task) -> Task:
        self.session.add(task)
        self.session.commit()
        return task

    def get_all_tasks_db(self, user_id: int):
        return self.session.query(Task).filter_by(user_id=user_id).all()

    def get_task_by_id_db(self, task_id: int, user_id: int):
        return self.session.query(Task).filter_by(task_id=task_id, user_id=user_id).first()

    def update_task_db(self, task: Task):
        task = self.session.merge(task)
        self.session.commit()
        return self.session.commit()

    def delete_task_db(self, task) -> None:
        self.session.delete(task)
        self.session.commit()
