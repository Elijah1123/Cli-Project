# contest.py
"""
Contest entry point for the TaskManager CLI project.

This script makes it easy to run the CLI with:
    pipenv run python contest.py <command> [options]

It imports the CLI group from src/taskmanager/cli.py and executes it.
"""

import sys
from src.taskmanager.cli import cli

if __name__ == "__main__":
    # Forward all CLI arguments to Click
    sys.exit(cli())
