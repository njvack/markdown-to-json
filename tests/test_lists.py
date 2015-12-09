# -*- coding: utf-8 -*-

import pytest


from markdown_to_json.vendor import CommonMark
from markdown_to_json import dict_renderer, json_writer


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
    return json_writer.CMarkASTNester().nest(ast)


def test_nester_lists_correctly(list_nested):
    stringified = dict_renderer.Renderer().stringify_dict(list_nested)
    l = stringified['Heading']
    assert l == ['a', 'b', ['b.a', 'b.b'], 'c']
