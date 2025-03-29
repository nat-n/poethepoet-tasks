from pathlib import (
    Path,
)


def get_path(name: str) -> Path:
    return Path(__file__).parent / name
