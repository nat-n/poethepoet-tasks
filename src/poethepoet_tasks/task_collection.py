from __future__ import annotations

import inspect
from functools import partial
from typing import TYPE_CHECKING, Callable, get_args, get_origin, get_type_hints

from .helpers.docstrings import parse_args_from_docstring
from .helpers.inspection import arg_types as _arg_types
from .helpers.inspection import is_union

if TYPE_CHECKING:
    from collections.abc import Collection, Iterator


class TaskCollection:
    """
    Provides a convenient way to build up a collection of tasks,
    which can be directly referenced by from a poethepoet configuration.
    """

    def __init__(
        self, env: dict[str, str] | None = None, envfile: list[str] | None = None
    ):
        """
        Initialize a new TaskCollection

        :param env: Environment variables to set for tasks in this collection
        :param envfile: Env files for variables to set for tasks in this collection
        """
        self._env: dict[str, str] = env or {}
        self._envfile: list[str] = envfile or []
        self._tasks: dict[str, list[_TaskConfig]] = {}
        self.config_path = inspect.currentframe().f_back.f_globals.get("__file__")  # type: ignore[union-attr]

    @property
    def env(self) -> dict[str, str]:
        return self._env

    @property
    def envfile(self) -> list[str]:
        return self._envfile

    def add(self, task_name: str, task_config: dict, tags: Collection[str] = tuple()):
        """
        Add task configuration to the config

        :param task_name: The name of the task
        :param task_config: The task options
        :param tags:
            Tags to associate with the task for the purpose of filtering
        """
        self._tasks.setdefault(task_name, [])
        self._tasks[task_name].append(
            _TaskConfig(task_name, task_config, (*tags, f"task-{task_name}"))
        )

    def remove(self, task_name: str, tags: Collection[str] = tuple()):
        """
        Unregister all task configurations with the given name.
        If tags are provided, only remove tasks matching one or more of them.

        :param task_name: The name of the task to remove
        :param tags: If provided then only remove tasks with one or more of these tags
        """

        if task_name in self._tasks:
            if not tags:
                del self._tasks[task_name]
            else:
                self._tasks[task_name] = [
                    task
                    for task in self._tasks[task_name]
                    if not any(tag in task.tags for tag in tags)
                ]

    def include(self, other: TaskCollection):
        """
        Merge another TaskCollection into this one.

        :param other: The other TaskCollection to include
        """
        for key, value in other.env.items():
            if key not in self.env:
                self.env[key] = value

        for envfile in other.envfile:
            if envfile not in self.envfile:
                self.envfile.append(envfile)

        for task in other:
            self.add(task.name, task.options, task.tags)

    def __iter__(self) -> Iterator[_TaskConfig]:
        for task_variants in self._tasks.values():
            yield from task_variants

    def __call__(
        self,
        include_tags: Collection[str] = tuple(),
        exclude_tags: Collection[str] = tuple(),
    ) -> dict:
        """
        Output a JSON serializable representation that be loaded by poethepoet.

        Only the first task with a given name that is not filtered out based
        on include_tags or exclude_tags will be included.

        :param include_tags:
            Only include tasks with one or more of these tags.
            If not provided, include all tasks.
        :param exclude_tags: Exclude tasks with one or more of these tags

        :return: A JSON serializable representation of the task collection
        """
        result = {"env": self.env, "envfile": self.envfile}

        if self.config_path:
            result["config_path"] = self.config_path

        tasks: dict[str, dict] = {}
        for task_variants in self._tasks.values():
            for task in task_variants:
                if include_tags and not any(tag in task.tags for tag in include_tags):
                    continue
                if exclude_tags and any(tag in task.tags for tag in exclude_tags):
                    continue
                tasks[task.name] = task.options
                break
        result["tasks"] = tasks

        return result

    def script(
        self,
        func: Callable | None = None,
        *,
        task_name: str | None = None,
        help: str | None = None,
        task_args: bool = True,
        options: dict | None = None,
        tags: Collection[str] = tuple(),
    ):
        """
        A decorator to generate a script task from the decorated function.

        :param func: The function to decorate
        :param task_name:
            The name of the task. if not set then the function name is used
            (transformed to kebab-case).
        :param help:
            Documentation to display for this task.
            If not set then the function docstring is used.
        :param task_args: If True, infer task args from the function signature.
        :param options: Any other options to provide as config for the script task.
        :param tags: Tags to associate with the task for the purpose of filtering
        :return: The decorated function
        """

        if func is None:
            return partial(
                self.script,
                task_name=task_name,
                help=help,
                task_args=task_args,
                options=options,
                tags=tags,
            )

        task_config: dict = {
            **(options or {}),
            "script": f"{func.__module__}:{func.__name__}",
            "help": help or (func.__doc__ or "").strip().split("\n\n")[0],
        }

        if task_args:
            args: list[dict] = []
            args_help = parse_args_from_docstring(func.__doc__ or "")
            params = inspect.signature(func).parameters
            type_annotations = get_type_hints(func)
            has_positional = any(
                param.kind == param.KEYWORD_ONLY for param in params.values()
            )

            for param in params.values():
                arg = {"name": param.name, "positional": False}

                if param.name in args_help:
                    arg["help"] = args_help[param.name]
                if param.kind == param.POSITIONAL_ONLY:
                    arg["positional"] = True
                elif param.kind == param.POSITIONAL_OR_KEYWORD:
                    if has_positional:
                        arg["positional"] = True
                    else:
                        arg["options"] = ["--" + param.name.replace("_", "-")]
                elif param.kind == param.VAR_POSITIONAL:
                    arg["positional"] = True
                    arg["multiple"] = True
                elif param.kind == param.VAR_KEYWORD:
                    # Ignore **kwargs
                    continue
                else:
                    arg["options"] = ["--" + param.name.replace("_", "-")]

                if param.annotation != param.empty:
                    annotation = type_annotations[param.name]
                    if is_union(annotation):
                        annotation_args = get_args(annotation)
                        annotation = next(
                            (anno for anno in annotation_args if anno), None
                        )
                        is_nullable = type(None) in annotation_args
                    else:
                        if not arg["positional"] and get_origin(annotation) is list:
                            if annotation_args := get_args(annotation):
                                annotation = annotation_args[0]
                            else:
                                annotation = str
                            arg["multiple"] = True
                        is_nullable = False

                    if annotation in _arg_types:
                        arg["type"] = _arg_types[annotation]
                    else:
                        raise ValueError(
                            "Unsupported argument type for argument "
                            f"{param.name}: {annotation}"
                        )

                    if param.default == param.empty and not is_nullable:
                        arg["required"] = True

                if param.default != param.empty:
                    arg["default"] = param.default

                args.append(arg)
            task_config["args"] = args

        self.add(
            task_name=task_name or func.__name__.replace("_", "-").lower(),
            task_config=task_config,
            tags=tags,
        )

        return func


class _TaskConfig:
    name: str
    options: dict
    tags: Collection[str]

    def __init__(self, name: str, options: dict, tags: Collection[str]):
        self.name = name
        self.options = options
        self.tags = tags


__all__ = ["TaskCollection"]
