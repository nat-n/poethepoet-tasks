import re


def parse_args_from_docstring(docstring: str) -> dict[str, str]:
    """
    Parse the arguments from the docstring of a function.
    Supports rst and google style docstrings.

    :param docstring: The docstring to parse
    :return: A dictionary of argument names and their descriptions
    """

    if not docstring:
        return {}

    if ":param " in docstring:
        return parse_rst_docstring_params(docstring)

    return parse_google_docstring_args(docstring)


_PARAM_FIELD_RE = (
    r"^(?P<indent>[^\n]\s+)?"
    r":param\s+(?:(?P<type>\w+)\s)?(?P<name>\w+):"
    r"(?P<docline>.*?)$"
)


def parse_rst_docstring_params(docstring: str) -> dict[str, str]:
    """
    Parse the arguments from an rst-style docstring.

    :param docstring: The docstring to parse
    :return: A dictionary of argument names and their descriptions
    """

    result = {}
    indent_len = "0"
    current_arg = ""
    current_doc: list[str] = []
    for line in _unindent_docstring(docstring).splitlines():
        if match := re.match(_PARAM_FIELD_RE, line):
            if current_arg:
                result[current_arg] = " ".join(current_doc)
            current_arg = match.group("name")
            # Multiline docs must be indented more than the param line
            indent_len = str(len(match.group("indent") or "") + 1)
            current_doc = [match.group("docline").strip()]
        elif match := re.match(r"^\s{" + indent_len + r"}\s*(?P<docline>\w.*?)$", line):
            current_doc.append(match.group("docline").strip())
        elif current_arg:
            result[current_arg] = " ".join(current_doc)
            current_arg = ""

    if current_arg:
        result[current_arg] = " ".join(current_doc)

    return result


_GOOGLE_ARGS_SECTION_RE = r"(?ms)^Args:\s*\n(.*?\n)\n?$"
_GOOGLE_ARG_LINE_RE = r"(?P<indent> {2,4})(?P<name>\w+): (?P<docline>.+?)$"


def parse_google_docstring_args(docstring: str) -> dict[str, str]:
    """
    Parse the arguments from a google-style docstring.

    :param docstring: The docstring to parse
    :return: A dictionary of argument names and their descriptions
    """

    arg_section = re.search(_GOOGLE_ARGS_SECTION_RE, _unindent_docstring(docstring))
    if not arg_section:
        return {}

    result = {}
    indent_len = "0"
    current_arg = ""
    current_doc: list[str] = []
    for line in arg_section[1].splitlines():
        if match := re.match(_GOOGLE_ARG_LINE_RE, line):
            if current_arg:
                result[current_arg] = " ".join(current_doc)
            current_arg = match.group("name")
            # Multiline docs must be indented at least 2 spaces more than the first line
            indent_len = str(len(match.group("indent")) + 2)
            current_doc = [match.group("docline").strip()]
        elif match := re.match(r"^\s{" + indent_len + r"}\s*(?P<docline>\w.*?)$", line):
            current_doc.append(match.group("docline").strip())
        elif current_arg:
            result[current_arg] = " ".join(current_doc)
            current_arg = ""

    if current_arg:
        result[current_arg] = " ".join(current_doc)

    return result


def _unindent_docstring(docstring: str) -> str:
    """
    Unindent the docstring by removing the common leading whitespace.

    :param docstring: The docstring to unindent
    :return: The unindented docstring
    """
    if not docstring.strip():
        return ""
    common_indent = min(
        next((index for index, char in enumerate(line) if not char.isspace()), 0)
        for line in docstring.splitlines()
        if line.strip()
    )
    return "\n".join(line[common_indent:] for line in docstring.splitlines())
