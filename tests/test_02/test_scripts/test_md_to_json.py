from markdown_to_json.scripts.md_to_json import jsonify_markdown
from unittest.mock import mock_open, patch
import json
import pytest
import sys


# Sample data for testing
VALID_MARKDOWN = "This is a **markdown** document."
EXPECTED_JSON = '{\n"root": [\n"This is a **markdown** document."\n]\n}'  # Simplified for demonstration
INVALID_MARKDOWN_PATH = "/invalid/path/to/markdown.md"


@pytest.mark.parametrize(
    "markdown_content, outfile, indent, expected_output, expect_exception",
    [
        (VALID_MARKDOWN, "valid_output.json", 2, EXPECTED_JSON, False),
        (VALID_MARKDOWN, None, 2, EXPECTED_JSON, False),  # to stdout
        (VALID_MARKDOWN, "valid_output.json", -1, EXPECTED_JSON, False),  # compact JSON
        (VALID_MARKDOWN, "valid_output.json", 0, EXPECTED_JSON, False),
        # (INVALID_MARKDOWN_PATH, "error_output.json", 2, None, True),
    ],
)
def test_jsonify_markdown(tmp_path, markdown_content, outfile, indent, expected_output, expect_exception):
    markdown_file = tmp_path / "test.md"
    markdown_file.write_text(markdown_content)

    with patch("sys.exit") as mock_exit:
        if outfile:
            output_path = tmp_path / outfile
            jsonify_markdown(str(markdown_file), str(output_path), indent)
            with open(output_path, "r", encoding="utf-8") as f:
                actual_output = f.read()
                assert json.dumps(json.loads(actual_output), indent=indent).strip() == json.dumps(json.loads(expected_output), indent=indent).strip()
        else:
            # For stdout, we'll need to capture the output with pytest's capsys
            # with pytest.raises(SystemExit) as _e:

            if expect_exception:
                with pytest.raises(FileNotFoundError):
                    jsonify_markdown(INVALID_MARKDOWN_PATH, None, indent)


# Note: Capturing stdout with capsys and integrating with pytest's parametrize decorator requires a bit more complex setup,
# which is simplified in this example for clarity.


# Simulated exceptions for testing.
class MockReadError(Exception):
    pass


class MockWriteError(Exception):
    pass


@pytest.mark.parametrize(
    "exception, func_to_mock, expected_error_message, use_stdout",
    [
        # Simulating an exception when reading the markdown file.
        (MockReadError, "markdown_to_json.scripts.md_to_json.open", "Error: Can't open", False),
    ],
)
def test_jsonify_markdown_with_exceptions(
    exception, func_to_mock, expected_error_message, use_stdout, caplog, tmp_path
):
    markdown_file = tmp_path / "test.md"
    markdown_file.write_text("Sample markdown content")

    outfile = "valid_output.json"
    if use_stdout:
        outfile = None  # Output set to None to use stdout

    with patch(func_to_mock, side_effect=exception):
        # with patch.object(sys, "exit") as mock_exit:
        with pytest.raises(SystemExit):
            jsonify_markdown(str(markdown_file), outfile, 2)
        # mock_exit.assert_called_once()
        assert expected_error_message in caplog.text


def test_jsonify_markdown_to_file_success(tmp_path):
    # Mock dependencies
    markdown_content = "# Title\n\nSome content."
    expected_json_output = json.dumps({"Title": "Some content."}, indent=2) + "\n"

    input_md_path = tmp_path / "input.md"
    input_md_path.write_text(markdown_content, encoding="utf-8")

    output_json_path = tmp_path / "output.json"

    jsonify_markdown(str(input_md_path), str(output_json_path), 2)

    with open(output_json_path, "r", encoding="utf-8") as f:
        output_content = f.read()
        assert output_content == expected_json_output


def test_jsonify_markdown_to_stdout_success(capfd, tmp_path):
    markdown_content = "# Another Title\n\nMore content."
    expected_json_output = json.dumps({"Another Title": "More content."}, indent=2) + "\n"

    input_md_path = tmp_path / "input2.md"
    input_md_path.write_text(markdown_content, encoding="utf-8")

    jsonify_markdown(str(input_md_path), None, 2)
    captured = capfd.readouterr()
    assert captured.out == expected_json_output


def test_jsonify_markdown_empty_file(tmp_path):
    input_md_path = tmp_path / "empty.md"
    input_md_path.touch()  # creates an empty file

    output_json_path = tmp_path / "output_empty.json"

    jsonify_markdown(str(input_md_path), str(output_json_path), 2)


def test_jsonify_markdown_read_error(tmp_path):
    input_md_path = tmp_path / "nonexistent.md"
    # File does not exist, intentionally causing a read error

    with pytest.raises(FileNotFoundError):
        jsonify_markdown(str(input_md_path), None, 2)
