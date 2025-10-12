from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    ForeignKey,
    Date,
    TIMESTAMP,
    text
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    role = Column(String)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    tasks = relationship("Task", back_populates="user")


class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True)
    task_name = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    status = Column(Enum("pending", "in-progress", "completed", name="task_status"), server_default="pending")
    due_date = Column(Date)
    priority = Column(Enum("low", "medium", "high", name="task_priority"), server_default="medium")

    user = relationship("User", back_populates="tasks")
