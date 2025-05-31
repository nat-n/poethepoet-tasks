from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from poethepoet_tasks.task_collection import TaskCollection


@pytest.fixture(scope="session")
def assert_tasks_match():
    """
    Fixture to assert that the tasks match the expected tasks, accounting for the fact
    that the config_path is unstable across environments.
    """

    def _assert_tasks_match(tasks: "TaskCollection", rendered_config: dict):
        actual_config = tasks()
        actual_config["config_path"] = (
            actual_config["config_path"].replace("\\", "/").split("tests")[-1]
        )
        excepted_config = rendered_config.copy()
        excepted_config["config_path"] = excepted_config["config_path"].split("tests")[
            -1
        ]

        assert actual_config == excepted_config, (
            f"Expected tasks to match, but got:\n{actual_config}\n\n"
            f"Expected:\n{excepted_config}"
        )

    return _assert_tasks_match
