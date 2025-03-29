from .resources import get_path
from .task_collection import TaskCollection

tasks = TaskCollection()

tasks.add(
    task_name="format",
    task_config={
        "sequence": ["format-ruff $files", "format-black $files"],
        "help": "Run ruff fixer on code base",
        "args": [
            {
                "name": "files",
                "positional": True,
                "multiple": True,
                "help": "The files to format",
                "default": "src tests",
            }
        ],
    },
    tags=["ruff", "black"],
)

tasks.add(
    task_name="format",
    task_config={
        "cmd": (
            'ruff check --config="${RUFF_CONFIG:-'
            + str(get_path("ruff.toml"))
            + '}" --fix-only $files'
        ),
        "help": "Run ruff fixer on the code base",
        "args": [
            {
                "name": "files",
                "positional": True,
                "multiple": True,
                "help": "The files to format",
                "default": "src tests",
            }
        ],
    },
    tags=["ruff"],
)

tasks.add(
    task_name="format",
    task_config={
        "cmd": "black $files",
        "help": "Run black on the code base",
        "args": [
            {
                "name": "files",
                "positional": True,
                "multiple": True,
                "help": "The files to format",
                "default": "src tests",
            }
        ],
    },
    tags=["black"],
)

tasks.add(
    task_name="format-ruff",
    task_config={
        "cmd": (
            'ruff check --config="${RUFF_CONFIG:-'
            + str(get_path("ruff.toml"))
            + '}" --fix-only $files'
        ),
        "help": "Run ruff fixer on the code base",
        "args": [
            {
                "name": "files",
                "positional": True,
                "multiple": True,
                "help": "The files to format",
                "default": "src tests",
            }
        ],
    },
    tags=["black", "ruff"],
)

tasks.add(
    task_name="format-black",
    task_config={
        "cmd": "black $files",
        "help": "Run black on the code base",
        "args": [
            {
                "name": "files",
                "positional": True,
                "multiple": True,
                "help": "The files to format",
                "default": "src tests",
            }
        ],
    },
    tags=["black", "ruff"],
)

tasks.add(
    task_name="lint",
    task_config={
        "help": "Run ruff fixer on code base",
        "cmd": 'ruff check --config="${RUFF_CONFIG:-'
        + str(get_path("ruff.toml"))
        + '}" $files',
        "args": [
            {
                "name": "files",
                "positional": True,
                "multiple": True,
                "help": "The files to format",
                "default": "src",
            }
        ],
    },
    tags=["ruff"],
)

tasks.add(
    task_name="style",
    task_config={
        "help": "Validate black code style",
        "cmd": "black $files --check --diff",
        "args": [
            {
                "name": "files",
                "positional": True,
                "multiple": True,
                "help": "The files to format",
                "default": "src",
            }
        ],
    },
    tags=["black"],
)

tasks.add(
    task_name="types",
    task_config={
        "help": "Run the type checker",
        "cmd": "mypy --ignore-missing-imports $files",
        "args": [
            {
                "name": "files",
                "positional": True,
                "multiple": True,
                "help": "The files to format",
                "default": "src",
            }
        ],
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
    task_name="check",
    task_config={
        "help": "Run all checks on the code base",
        "sequence": ["lint", "style", "types", "test"],
    },
    tags=["types", "test", "pytest", "lint", "ruff", "black"],
)

tasks.add(
    task_name="check",
    task_config={
        "help": "Run all checks on the code base",
        "sequence": ["lint", "types", "test"],
    },
    tags=["types", "test", "pytest", "lint", "ruff"],
)

tasks.add(
    task_name="check",
    task_config={
        "help": "Run all checks on the code base",
        "sequence": ["types", "test"],
    },
    tags=["types", "test", "pytest"],
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
