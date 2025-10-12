from models import User


class UserRepository:
    def __init__(self, session):
        self.session = session

    def create_user_db(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        return user

    def update_user_db(self, user: User) -> None:
        user = self.session.merge(user)
        self.session.commit()
        return self.session.commit()

    def get_user_by_id_db(self, user_id: int) -> None:
        return self.session.query(User).filter_by(id=user_id).first()

    def delete_user_db(self, user: User) -> None:
        self.session.delete(user)
        self.session.commit()
