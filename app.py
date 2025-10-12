from dataclasses import dataclass

from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models import Base
from services.task_service import TaskService
from repository.task_repository import TaskRepository


@dataclass
class Settings:
    DATABASE_URL: str


class AppFlask(Flask):
    def __init__(
        self,
        import_name,
        settings: Settings,
        static_url_path=None,
        static_folder="static",
        static_host=None,
        host_matching=False,
        subdomain_matching=False,
        template_folder="templates",
        instance_path=None,
        instance_relative_config=False,
        root_path=None,
    ) -> None:
        super().__init__(
            import_name,
            static_url_path,
            static_folder,
            static_host,
            host_matching,
            subdomain_matching,
            template_folder,
            instance_path,
            instance_relative_config,
            root_path,
        )

        self._settings = settings

    def run(self, *args, **kwargs) -> None:
        # database
        engine = create_engine(self._settings.DATABASE_URL)
        Base.metadata.create_all(engine)

        # session setup
        self._session = scoped_session(sessionmaker(engine))
        Base.query = self._session.query_property()

        # run method from base class
        super().run(*args, **kwargs)


settings = Settings(DATABASE_URL="postgresql://admin:admin@localhost:5434/po_db")

app = AppFlask(__name__, settings=settings)
repo = TaskRepository(app._session)
service = TaskService(repo)


if __name__ == "__main__":
    app.run(debug=True, port=8080)