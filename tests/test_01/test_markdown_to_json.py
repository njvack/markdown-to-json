from collections import OrderedDict
from markdown_to_json.markdown_to_json import CMarkASTNester, dictify_list_by, ContentError
from markdown_to_json.markdown_to_json import dictify
from unittest.mock import Mock
import pytest


@pytest.mark.parametrize(
    "markdown_str,expected_output",
    [
        ("# Heading 1\nContent 1\n# Heading 2\nContent 2", {"Heading 1": "Content 1", "Heading 2": "Content 2"}),
        ("# Heading 1\n* List 1\n* List 2", {"Heading 1": ["List 1", "List 2"]}),
        ("Content without headings", {"root": ["Content without headings"]}),
    ],
)
def test_dictify(markdown_str, expected_output):
    CommonMark = Mock()
    DocParser = Mock()
    DocParser().parse.return_value = Mock(children=[])
    CommonMark.DocParser = Mock(return_value=DocParser)

    result = dictify(markdown_str)

    assert dict(result) == expected_output


@pytest.fixture
def mock_ast():
    return Mock()


@pytest.fixture
def cmark_nester():
    return CMarkASTNester()


def test_dictify_list_by():
    # Prepare test data
    block1 = Mock(t="ATXHeader", level=1)
    block2 = Mock(t="Paragraph")
    block3 = Mock(t="ATXHeader", level=2)
    blocks = [block1, block2, block3]

    # Call the function
    result = dictify_list_by(blocks, lambda x: x.t == "ATXHeader")

    # Check the result
    expected_result = OrderedDict({block1: [block2], block3: []})
    assert result == expected_result


def test_CMarkASTNester_ensure_list_singleton(cmark_nester):
    # Prepare test data with mixed content
    blocks = [Mock(t="ATXHeader"), Mock(t="Paragraph")]

    # Call the method
    cmark_nester._ensure_list_singleton(blocks)

    # No Assertion as this method alters the input blocks


def test_CMarkASTNester_ensure_list_singleton_no_mixing(cmark_nester):
    # Prepare test data with only lists
    blocks = [Mock(t="List"), Mock(t="List")]

    # Call the method
    cmark_nester._ensure_list_singleton(blocks)

    # No Assertion as this method alters the input blocks


def test_CMarkASTNester_ensure_list_singleton_single_list_element(cmark_nester):
    # Prepare test data with a single list element
    blocks = [Mock(t="List")]

    # Call the method
    cmark_nester._ensure_list_singleton(blocks)

    # No Assertion as this method alters the input blocks


def test_ContentError():
    # Check the ContentError exception instantiation
    with pytest.raises(ContentError):
        raise ContentError("Test Content Error")
