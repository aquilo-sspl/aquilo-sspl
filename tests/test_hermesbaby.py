import os
import pytest
import requests
import subprocess
import time
from pathlib import Path
import sys


def test_hello(cli_runner):

    from src.hermesbaby.__main__ import app

    result = cli_runner.invoke(app, ["hello"])
    assert result.exit_code == 0
    assert "Hello" in result.output


@pytest.mark.parametrize(
    "command_line",
    [
        "",
    ],
)
def test_help(cli_runner, command_line):

    from src.hermesbaby.__main__ import app

    result = cli_runner.invoke(app, command_line.split())
    assert result.exit_code == 0
    assert "Usage" in result.output


@pytest.mark.parametrize(
    "command_line",
    [
        f"{sys.executable} -m hermesbaby",
        f"poetry run hermesbaby",
        f"poetry run hb",
    ],
)
def test_entry_points(command_line):

    result = subprocess.run(
        command_line.split(),
        start_new_session=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )

    assert result.returncode == 0
    assert "Usage" in result.stdout


@pytest.mark.parametrize(
    "some_rel_path_as_str, option",
    [
        ("", ""),
        (".", ""),
        ("some/relative/path", ""),
        ("", "--template vscode_scratch"),
        (".", "--template vscode_scratch"),
        ("some/relative/path", "--template vscode_scratch"),
    ],
)
def test_task_new(cli_runner, temp_dir, some_rel_path_as_str, option):

    from src.hermesbaby.__main__ import app

    args = f"new {some_rel_path_as_str} {option}"

    result = cli_runner.invoke(app, args.split())

    some_rel_path = Path(some_rel_path_as_str)
    path_to_index_rst = temp_dir / some_rel_path / "docs" / "index.rst"

    assert (
        path_to_index_rst.exists()
    ), f"Project path does not exist: {path_to_index_rst}"


def test_task_html(cli_runner, temp_dir):

    from src.hermesbaby.__main__ import app

    # Run the "new" command to set up the project
    result = cli_runner.invoke(app, ["new"])
    assert result.exit_code == 0, "Setup failed"

    result = cli_runner.invoke(app, ["html"])

    index_html = temp_dir / "out" / "docs" / "html" / "index.html"

    assert index_html.exists(), f"Build output does not exist: {index_html}"
