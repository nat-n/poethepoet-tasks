# ruff: noqa: E501

from __future__ import annotations

from poethepoet_tasks.task_collection import TaskCollection


def test_optional_single_value_script_args(assert_tasks_match):
    tasks = TaskCollection()

    @tasks.script()
    def my_task(value1: str | None = None, value2: str = "lol"):
        print(f"Values: {value1}, {value2}")

    assert_tasks_match(
        tasks,
        {
            "env": {},
            "envfile": [],
            "config_path": "/Users/nat/Projects/poethepoet-tasks/tests/test_script_decorator.py",
            "tasks": {
                "my-task": {
                    "script": "test_script_decorator:my_task",
                    "help": "",
                    "args": [
                        {
                            "name": "value1",
                            "positional": False,
                            "options": ["--value1"],
                            "multiple": False,
                            "type": "string",
                            "required": False,
                        },
                        {
                            "name": "value2",
                            "positional": False,
                            "options": ["--value2"],
                            "multiple": False,
                            "type": "string",
                            "required": False,
                            "default": "lol",
                        },
                    ],
                }
            },
        },
    )


def test_multivalue_positional_script_args(assert_tasks_match):
    tasks = TaskCollection()

    @tasks.script()
    def my_task(*values: int):
        print(f"Values: {values}")

    print(tasks())

    assert_tasks_match(
        tasks,
        {
            "env": {},
            "envfile": [],
            "config_path": "/Users/nat/Projects/poethepoet-tasks/tests/test_script_decorator.py",
            "tasks": {
                "my-task": {
                    "script": "test_script_decorator:my_task",
                    "help": "",
                    "args": [
                        {
                            "name": "values",
                            "type": "integer",
                            "required": True,
                            "positional": True,
                            "multiple": True,
                        }
                    ],
                }
            },
        },
    )


def test_nullable_required_script_arg(assert_tasks_match):
    tasks = TaskCollection()

    @tasks.script()
    def my_task(value: str | None):
        print(f"Value: {value}")

    assert_tasks_match(
        tasks,
        {
            "env": {},
            "envfile": [],
            "config_path": "/Users/nat/Projects/poethepoet-tasks/tests/test_script_decorator.py",
            "tasks": {
                "my-task": {
                    "script": "test_script_decorator:my_task",
                    "help": "",
                    "args": [
                        {
                            "name": "value",
                            "positional": False,
                            "options": ["--value"],
                            "multiple": False,
                            "type": "string",
                            "required": True,
                        }
                    ],
                }
            },
        },
    )


def test_arg_types_with_help(assert_tasks_match):
    tasks = TaskCollection()

    @tasks.script(tags=["hello"], task_args=True)
    def hello(
        huh: str | None = None,
        *,
        foo: int = 1,
        bar_bar: float = 1.0,
        baz: bool = True,
        qux: str = True,  # type: ignore[assignment]
    ):
        """
        Greet all the things

        :param huh: The thing to greet
        :param foo: The foo to greet
        :param bar_bar: The bar to greet
        :param baz: The baz to greet
        :param qux: The qux to greet
        """
        print("Hello, world!", huh, [qux])

    assert_tasks_match(
        tasks,
        {
            "env": {},
            "envfile": [],
            "config_path": "/Users/nat/Projects/poethepoet-tasks/tests/test_script_decorator.py",
            "tasks": {
                "hello": {
                    "script": "test_script_decorator:hello",
                    "help": "Greet all the things",
                    "args": [
                        {
                            "name": "huh",
                            "type": "string",
                            "required": False,
                            "positional": True,
                            "multiple": False,
                            "help": "The thing to greet",
                        },
                        {
                            "name": "foo",
                            "type": "integer",
                            "required": False,
                            "positional": False,
                            "multiple": False,
                            "help": "The foo to greet",
                            "default": 1,
                            "options": ["--foo"],
                        },
                        {
                            "name": "bar_bar",
                            "type": "float",
                            "required": False,
                            "positional": False,
                            "multiple": False,
                            "help": "The bar to greet",
                            "default": 1.0,
                            "options": ["--bar-bar"],
                        },
                        {
                            "name": "baz",
                            "type": "boolean",
                            "required": False,
                            "positional": False,
                            "multiple": False,
                            "help": "The baz to greet",
                            "default": True,
                            "options": ["--baz"],
                        },
                        {
                            "name": "qux",
                            "type": "string",
                            "required": False,
                            "positional": False,
                            "multiple": False,
                            "help": "The qux to greet",
                            "default": True,
                            "options": ["--qux"],
                        },
                    ],
                }
            },
        },
    )
