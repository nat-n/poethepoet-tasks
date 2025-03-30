from poethepoet_tasks.helpers.docstrings import (
    parse_args_from_docstring,
    parse_google_docstring_args,
    parse_rst_docstring_params,
)


def test_parse_args_from_docstring_rst():
    docstring = """
    Parse the arguments from an rst-style docstring.

    :param docstring: The docstring to parse
    :param another_param: Another parameter description
    :return: A dictionary of argument names and their descriptions
    """
    expected = {
        "docstring": "The docstring to parse",
        "another_param": "Another parameter description",
    }
    assert parse_args_from_docstring(docstring) == expected


def test_parse_args_from_docstring_google():
    docstring = """
    Parse the arguments from a google-style docstring.

    Args:
      docstring: The docstring to parse
      another_param: Another parameter description

    Returns:
      A dictionary of argument names and their descriptions
    """
    expected = {
        "docstring": "The docstring to parse",
        "another_param": "Another parameter description",
    }
    assert parse_args_from_docstring(docstring) == expected


def test_parse_rst_docstring_params():
    docstring = """
    :param param1: Description for param1
    :param param2: Description for param2
    """
    expected = {
        "param1": "Description for param1",
        "param2": "Description for param2",
    }
    assert parse_rst_docstring_params(docstring) == expected


def test_parse_rst_docstring_single_param():
    docstring = """
    :param param1: Description for param1
    """
    expected = {"param1": "Description for param1"}
    assert parse_rst_docstring_params(docstring) == expected


def test_parse_google_docstring_args():
    docstring = """
    Args:
        param1: Description for param1
        param2: Description for param2
    """
    expected = {
        "param1": "Description for param1",
        "param2": "Description for param2",
    }
    assert parse_google_docstring_args(docstring) == expected


def test_parse_google_docstring_single_arg():
    docstring = """
    Args:
        param1: Description for param1
    """
    expected = {"param1": "Description for param1"}
    assert parse_google_docstring_args(docstring) == expected


def test_parse_args_from_docstring_empty():
    docstring = ""
    expected = {}
    assert parse_args_from_docstring(docstring) == expected


def test_parse_rst_docstring_params_multiline():
    docstring = """
    :param param1: Description for param1
        that spans multiple lines
    :param param2: Another description
    """
    expected = {
        "param1": "Description for param1 that spans multiple lines",
        "param2": "Another description",
    }
    assert parse_rst_docstring_params(docstring) == expected


def test_parse_google_docstring_args_multiline():
    docstring = """
    Args:
        param1: Description for param1
                that spans multiple lines
        param2: Another description
    """
    expected = {
        "param1": "Description for param1 that spans multiple lines",
        "param2": "Another description",
    }
    assert parse_google_docstring_args(docstring) == expected
