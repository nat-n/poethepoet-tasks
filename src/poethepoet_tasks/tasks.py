"""
This module demonstrates creating a TaskCollection, including:
- multiple definitions for some tasks, which definition is used depends on order and the
  included/excluded tags.
- using generators to lazily define tasks based on tags and arbitrary logic.
"""

from .resources import get_path
from .tags import TagEvaluator
from .task_collection import TaskCollection

RUFF_TOML_PATH = str(get_path("ruff.toml"))


def _files_arg(default="src"):
    return {
        "name": "files",
        "positional": True,
        "multiple": True,
        "help": "The files to format",
        "default": default,
    }


tasks = TaskCollection()


tasks.add(
    task_name="lint",
    task_config={
        "help": "Run ruff linter on code base",
        "cmd": 'ruff check --config="${RUFF_CONFIG:-' + RUFF_TOML_PATH + '}" $files',
        "args": [_files_arg(default="src tests")],
    },
    tags=["lint", "test", "ruff"],
)

tasks.add(
    task_name="lint",
    task_config={
        "help": "Run ruff linter on code base",
        "cmd": 'ruff check --config="${RUFF_CONFIG:-' + RUFF_TOML_PATH + '}" $files',
        "args": [_files_arg()],
    },
    tags=["lint", "ruff"],
)

tasks.add(
    task_name="style",
    task_config={
        "help": "Validate black code style",
        "cmd": "black $files --check --diff",
        "args": [_files_arg(default="src tests")],
    },
    tags=["style", "test", "black"],
)

tasks.add(
    task_name="style",
    task_config={
        "help": "Validate black code style",
        "cmd": "black $files --check --diff",
        "args": [_files_arg()],
    },
    tags=["style", "black"],
)

tasks.add(
    task_name="types",
    task_config={
        "help": "Run the type checker",
        "cmd": "mypy --ignore-missing-imports $files",
        "args": [_files_arg(default="src tests")],
    },
    tags=["test", "mypy"],
)

tasks.add(
    task_name="types",
    task_config={
        "help": "Run the type checker",
        "cmd": "mypy --ignore-missing-imports $files",
        "args": [_files_arg()],
    },
    tags=["mypy"],
)

tasks.add(
    task_name="test",
    task_config={
        "help": "Run tests",
        "cmd": "pytest",
    },
    tags=["pytest"],
)


tasks.add(
    task_name="clean",
    task_config={
        "script": """
          poethepoet.scripts:rm(
            ".coverage",
            ".ruff_cache",
            ".mypy_cache",
            ".pytest_cache",
            "./**/__pycache__",
            "dist",
            "htmlcov",
            verbosity=environ.get('POE_VERBOSITY'),
            dry_run=_dry_run
          )
        """,
        "help": "Remove generated files",
    },
)


@tasks.generate
def generate_format_tasks(requested_tags: TagEvaluator):
    """
    Generate tasks for code formatting based on whether ruff or black are
    """

    files_arg = _files_arg(
        default="src tests" if requested_tags.evaluate("test") else "src"
    )
    ruff_cmd = (
        'ruff check --config="${RUFF_CONFIG:-' + RUFF_TOML_PATH + '}" --fix-only $files'
    )
    black_cmd = "black $files"

    if requested_tags.all("ruff", "black"):
        yield "format", {
            "sequence": ["format-ruff $files", "format-black $files"],
            "help": "Run ruff and black formatters on the code base",
            "args": [files_arg],
        }
        yield "format-ruff", {
            "cmd": ruff_cmd,
            "help": "Run ruff formatter on the code base",
            "args": [files_arg],
        }
        yield "format-black", {
            "cmd": black_cmd,
            "help": "Run black formatter on the code base",
            "args": [files_arg],
        }
    elif requested_tags.evaluate("ruff"):
        yield "format", {
            "cmd": ruff_cmd,
            "help": "Run ruff formatter on the code base",
            "args": [files_arg],
        }
    elif requested_tags.evaluate("black"):
        yield "format", {
            "cmd": black_cmd,
            "help": "Run black formatter on the code base",
            "args": [files_arg],
        }


@tasks.generate
def generate_check_task(requested_tags: TagEvaluator):
    """
    Generates `check` task as a sequence including `lint`, `style`, `types`, and `test`
    tasks in that order, excluding any tasks that are explicitly excluded a
    `task-<taskname>` tag.

    If all referenced tasks are excluded then no check task is generated.
    """

    task_name = "check"
    doc = "Run all checks on the code base"
    sequence = []
    if not requested_tags.excluded("task-lint"):
        sequence.append("lint")
    if not requested_tags.excluded("task-style"):
        sequence.append("style")
    if not requested_tags.excluded("task-types"):
        sequence.append("types")
    if not requested_tags.excluded("task-test") and not requested_tags.excluded("test"):
        sequence.append("test")

    if sequence:
        yield task_name, {"help": doc, "sequence": sequence}
