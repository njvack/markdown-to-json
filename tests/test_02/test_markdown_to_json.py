from markdown_to_json.markdown_to_json import jsonify
from markdown_to_json.markdown_to_json import ContentError
from unittest.mock import patch
from unittest.mock import Mock
import json
import pytest


# Simulate an exception scenario for markdown parsing
@patch("markdown_to_json.markdown_to_json.CommonMark.DocParser.parse")
def test_jsonify_with_parsing_exception(mock_parse):
    # Configure the mock to raise an exception when called
    mock_parse.side_effect = ContentError("Parsing failed")

    with pytest.raises(ContentError) as excinfo:
        jsonify("# This markdown causes parsing to fail")

    # Optionally, check the exception message if needed
    assert "Parsing failed" in str(excinfo.value)

    mock_parse.assert_called_once()


# Helper function to create a mock block that mimics CommonMark's block structure
def create_mock_block(t="Paragraph", level=None, string_content="", children=None):
    block = Mock()
    block.t = t
    block.level = level
    block.string_content = string_content
    block.children = children or []
    return block


def test_jsonify_happy_path():
    # Now call jsonify and check if it processes our AST correctly
    markdown_str = "# Header\n\nParagraph under header"
    expected_json_str = json.dumps({"Header": "Paragraph under header"})

    # Act
    json_output = jsonify(markdown_str)

    # Assert
    assert json_output == expected_json_str


def test_jsonify_empty_markdown():
    # Test the behavior with an empty markdown string, expecting an empty JSON object
    markdown_str = ""
    expected_json_str = json.dumps({"root": []})
    actual_json_str = jsonify(markdown_str)
    assert actual_json_str == expected_json_str


def test_jsonify_with_parsing_failure():
    # Simulate a parsing failure scenario
    with patch("markdown_to_json.markdown_to_json.CommonMark.DocParser.parse", side_effect=ValueError("Parsing Error")):
        with pytest.raises(ValueError) as exc_info:
            markdown_str = "This will fail to parse"
            jsonify(markdown_str)

        assert "Parsing Error" in str(exc_info.value)
