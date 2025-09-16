# src/tests/test_cli.py
import pytest
from click.testing import CliRunner
from taskmanager.cli import cli
from taskmanager.db import drop_db, init_db

@pytest.fixture(autouse=True)
def clean_db():
    """Reset the database before each CLI test."""
    drop_db()
    init_db()
    yield
    drop_db()

def test_initdb():
    runner = CliRunner()
    result = runner.invoke(cli, ["initdb"])
    assert result.exit_code == 0
    assert "Database initialized" in result.output

def test_add_user_and_project_and_task():
    runner = CliRunner()

    # create db
    runner.invoke(cli, ["initdb"])

    # add user
    result = runner.invoke(cli, ["add_user", "alice", "--email", "alice@example.com"])
    assert result.exit_code == 0
    assert "Created user" in result.output

    # add project
    result = runner.invoke(cli, ["add_project", "alice", "Website", "--description", "Build site"])
    assert result.exit_code == 0
    assert "Created project" in result.output

    # add task
    result = runner.invoke(cli, ["add_task", "1", "Write README"])
    assert result.exit_code == 0
    assert "Task created" in result.output

    # list tasks
    result = runner.invoke(cli, ["list_tasks"])
    assert result.exit_code == 0
    assert "Write README" in result.output

def test_complete_task():
    runner = CliRunner()
    runner.invoke(cli, ["initdb"])
    runner.invoke(cli, ["add_user", "bob"])
    runner.invoke(cli, ["add_project", "bob", "TestProj"])
    runner.invoke(cli, ["add_task", "1", "TestTask"])

    # complete task
    result = runner.invoke(cli, ["complete", "1"])
    assert result.exit_code == 0
    assert "Marked done" in result.output

    # check list shows completed
    result = runner.invoke(cli, ["list_tasks"])
    assert "True" in result.output  # completed column
