# Part of the markdown_to_json package
# Written by Nate Vack <njvack@freshforever.net>
# Copyright 2023 Board of Regents of the University of Wisconsin System

import pytest

from markdown_to_json.vendor import CommonMark
from markdown_to_json.markdown_to_json import Renderer, CMarkASTNester


@pytest.fixture
def list_md():
    return """
# Heading

* a
* b
    * b.a
    * b.b
* c
"""


@pytest.fixture
def list_nested(list_md):
    ast = CommonMark.DocParser().parse(list_md)
    return CMarkASTNester().nest(ast)


def test_nester_lists_correctly(list_nested):
    stringified = Renderer().stringify_dict(list_nested)
    list_value = stringified["Heading"]
    assert list_value == ["a", "b", ["b.a", "b.b"], "c"]
