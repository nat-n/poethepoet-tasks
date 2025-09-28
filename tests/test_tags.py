from poethepoet_tasks.tags import TagEvaluator


def test_tag_evaluator_evaluate():
    tags = TagEvaluator(include_tags=["foo", "bar", "baz"], exclude_tags=["baz", "qux"])

    assert tags.evaluate("foo") is True
    assert tags.evaluate("foo", "bar") is True
    assert tags.evaluate("foo", "baz") is False
    assert tags.evaluate("qux") is False
    assert tags.evaluate("foo", "unknown") is True
    assert tags.evaluate("unknown") is False


def test_tag_evaluator_all():
    tags = TagEvaluator(include_tags=["foo", "bar", "baz"], exclude_tags=["baz", "qux"])

    assert tags.all("foo") is True
    assert tags.all("foo", "bar") is True
    assert tags.all("foo", "baz") is False
    assert tags.all("baz") is False
    assert tags.all("qux", "unknown") is False
    assert tags.all("unknown") is False
    assert tags.all("foo", "unknown") is False


def test_tag_evaluator_excluded():
    tags = TagEvaluator(include_tags=["foo", "bar", "baz"], exclude_tags=["baz", "qux"])

    assert tags.excluded("foo") is False
    assert tags.excluded("bar") is False
    assert tags.excluded("baz") is True
    assert tags.excluded("qux") is True
    assert tags.excluded("unknown") is False


def test_empty_tag_evaluator():
    tags = TagEvaluator()

    assert tags.evaluate("foo", "bar") is True
    assert tags.all("foo", "bar") is True
    assert tags.excluded("foo") is False


def test_include_only_tag_evaluator():
    tags = TagEvaluator(include_tags=["foo", "bar"])

    assert tags.evaluate("foo") is True
    assert tags.evaluate("foo", "bar") is True
    assert tags.all() is True
    assert tags.all("foo", "bar") is True
    assert tags.all("foo", "bar", "unknown") is False
    assert tags.excluded("unknown") is False


def test_exclude_only_tag_evaluator():
    tags = TagEvaluator(exclude_tags=["baz", "qux"])

    assert tags.evaluate("unknown") is True
    assert tags.evaluate("baz") is False
    assert tags.evaluate("baz", "qux") is False
    assert tags.all("baz") is False
    assert tags.all("baz", "unknown") is False
    assert tags.all("unknown") is True
    assert tags.excluded("baz") is True
    assert tags.excluded("unknown") is False
