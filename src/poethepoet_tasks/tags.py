from collections.abc import Collection


class TagEvaluator:
    """
    Helps evaluate tag inclusion and exclusion logic
    """

    def __init__(
        self,
        include_tags: Collection[str] = tuple(),
        exclude_tags: Collection[str] = tuple(),
    ):
        self.include_tags: Collection[str] = include_tags
        self.exclude_tags: Collection[str] = exclude_tags

    def evaluate(self, *task_tags: str) -> bool:
        """
        Evalute whether a task with the given tags should be included or not.

        :return: True if a task with these tags should be included, otherwise False
        """

        if self.include_tags and not any(tag in task_tags for tag in self.include_tags):
            return False
        return not any(tag in task_tags for tag in self.exclude_tags)

    def all(self, *tags: str) -> bool:
        """
        Check if all the given tags are included and not excluded.

        :return: True if all the given tags evaluate to True, otherwise False.
        """

        if self.include_tags and not all(tag in self.include_tags for tag in tags):
            return False
        return not any(tag in tags for tag in self.exclude_tags)

    def excluded(self, tag: str) -> bool:
        """
        Check if the given tag is explicitly excluded

        :return: True if the tag is exluded, otherwise False
        """

        return tag in self.exclude_tags
