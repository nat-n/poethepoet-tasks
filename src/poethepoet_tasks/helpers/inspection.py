import sys
from typing import Any, Union, get_origin

arg_types = {
    int: "integer",
    float: "float",
    str: "string",
    bool: "boolean",
}


def is_union(annotation: Any) -> bool:
    """
    Determines if the given annotation is a union type.

    :param annotation: The type annotation to inspect.
    :returns: ``True`` if the annotation is a union type, ``False`` otherwise.
    """
    if sys.version_info >= (3, 10):
        from types import (
            UnionType,
        )

        if get_origin(annotation) is UnionType:
            return True
    return get_origin(annotation) is Union
