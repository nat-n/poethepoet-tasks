from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

from .task_collection import TaskCollection

__all__ = ["TaskCollection"]


def tasks(include_tags: Sequence[str] = tuple(), exclude_tags: Sequence[str] = tuple()):
    from .tasks import tasks

    return tasks(include_tags=include_tags, exclude_tags=exclude_tags)
