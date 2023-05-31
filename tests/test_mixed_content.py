import glob

from markdown_to_json.markdown_to_json import Renderer, CMarkASTNester
from markdown_to_json.vendor.CommonMark import CommonMark
from tests.util import locate_file


def test_mixed():
    absolute_file_paths = []
    for file in glob.glob(locate_file("../examples/mixed", __file__) + "/*.md"):
        sample_search_results_file: str = locate_file(file, __file__)
        absolute_file_paths.append(sample_search_results_file)
    assert absolute_file_paths

    for file_name in absolute_file_paths:
        with open(file_name, encoding="utf-8") as file:
            ast = CommonMark.DocParser().parse(file.read())
            dictionary = CMarkASTNester().nest(ast)
            stringified = Renderer().stringify_dict(dictionary)
            assert stringified


def test_issue_4():
    value = """## GUID

2db62bb2-8ac0-4137-b26f-78a12bff449d

## Title

Some title

## Summary

A Summary

## Priority

- Must

## Detailed Description

- Lorem Ipsum Blabla
- Lorem Ipsum Blabla 

## Reference Requirements

> na

## Categories

- Cat6
"""
    ast = CommonMark.DocParser().parse(value)
    dictionary = CMarkASTNester().nest(ast)
    stringified = Renderer().stringify_dict(dictionary)
    # Result isn't sensible though...
    assert stringified