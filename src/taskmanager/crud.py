# src/taskmanager/crud.py
from sqlalchemy import select
from .models import User, Project, Task
from .db import SessionLocal

def create_user(username: str, email: str | None = None):
    with SessionLocal() as session:
        user = User(username=username.strip(), email=(email.strip() if email else None))
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

def get_user_by_username(username: str):
    with SessionLocal() as session:
        stmt = select(User).where(User.username == username)
        return session.scalar(stmt)

def create_project(owner_username: str, title: str, description: str | None = None):
    with SessionLocal() as session:
        user = session.query(User).filter_by(username=owner_username).first()
        if not user:
            raise ValueError("Owner does not exist")
        project = Project(title=title.strip(), description=description, owner=user)
        session.add(project)
        session.commit()
        session.refresh(project)
        return project

def create_task(project_id: int, title: str, details: str | None = None):
    with SessionLocal() as session:
        project = session.get(Project, project_id)
        if not project:
            raise ValueError("Project not found")
        task = Task(title=title.strip(), details=details, project=project)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

def list_tasks(project_id: int = None):
    with SessionLocal() as session:
        stmt = select(Task)
        if project_id:
            stmt = stmt.where(Task.project_id == project_id)
        return session.scalars(stmt).all()

def mark_task_complete(task_id: int):
    with SessionLocal() as session:
        task = session.get(Task, task_id)
        if not task:
            raise ValueError("Task not found")
        task.completed = True
        session.commit()
        return task
