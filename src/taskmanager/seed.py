# src/taskmanager/seed.py
from .db import init_db
from .crud import create_user, create_project, create_task

def seed():
    init_db()
    u = create_user("alice", "alice@example.com")
    p = create_project("alice", "Website", "Launch site")
    create_task(p.id, "Write README")
    create_task(p.id, "Add tests")

if __name__ == "__main__":
    seed()
    print("Seed complete")
