# src/taskmanager/cli.py
import click
from tabulate import tabulate
from taskmanager.db import init_db
from taskmanager import crud


@click.group()
def cli():
    """TaskManager CLI"""
    pass


@cli.command()
def initdb():
    """Initialize the database"""
    init_db()
    click.echo("Database initialized.")


@cli.command()
@click.argument("username")
@click.option("--email", default=None, help="User email")
def add_user(username, email):
    user = crud.create_user(username, email)
    click.echo(f"Created user: {user.username} (id={user.id})")


@cli.command()
@click.argument("username")
@click.argument("title")
@click.option("--description", default="", help="Project description")
def add_project(username, title, description):
    try:
        project = crud.create_project(username, title, description)
        click.echo(f"Created project: {project.title} (id={project.id})")
    except ValueError as e:
        click.echo(f"Error: {e}")


@cli.command()
@click.argument("project_id", type=int)
@click.argument("title")
@click.option("--details", default="", help="Task details")
def add_task(project_id, title, details):
    try:
        task = crud.create_task(project_id, title, details)
        click.echo(f"Task created: {task.title} (id={task.id})")
    except ValueError as e:
        click.echo(f"Error: {e}")


@cli.command()
@click.option("--project-id", default=None, type=int)
def list_tasks(project_id):
    tasks = crud.list_tasks(project_id)
    table = [(t.id, t.title, t.completed, t.project_id) for t in tasks]
    click.echo(tabulate(table, headers=["id", "title", "completed", "project_id"]))


@cli.command()
@click.argument("task_id", type=int)
def complete(task_id):
    try:
        task = crud.mark_task_complete(task_id)
        click.echo(f"Marked done: {task.id} {task.title}")
    except ValueError as e:
        click.echo(f"Error: {e}")


if __name__ == "__main__":
    cli()
