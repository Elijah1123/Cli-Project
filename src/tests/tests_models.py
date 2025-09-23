# src/tests/test_models.py
import tempfile
import os
from taskmanager.db import ENGINE_URL, engine, SessionLocal, init_db, drop_db
from taskmanager.models import Base
from taskmanager.crud import create_user, create_project, create_task, list_tasks, mark_task_complete

def test_create_user_and_project_and_task(tmp_path, monkeypatch):
    # use a temp sqlite file for isolation
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("TASKMANAGER_DB", f"sqlite:///{db_path}")
    # Recreate engine if your code reads env var; otherwise just use init_db()
    init_db()

    u = create_user("bob", "bob@example.com")
    assert u.username == "bob"
    p = create_project("bob", "Alpha", "desc")
    assert p.title == "Alpha"
    t = create_task(p.id, "Task1")
    assert t.title == "Task1"

    tasks = list_tasks(p.id)
    assert len(tasks) >= 1

    mark_task_complete(t.id)
    tasks2 = list_tasks(p.id)
    assert any(i.completed for i in tasks2)
