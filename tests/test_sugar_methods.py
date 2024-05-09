import pytest as pytest

import markdown_to_json


@pytest.fixture
def simple_md():
    return """
# People

* Alice
* Bob
"""


def test_dictify(simple_md):
    dict_out = markdown_to_json.dictify(simple_md)
    assert hasattr(dict_out, "keys")
    assert "People" in dict_out


def test_jsonify(simple_md):
    json_out = markdown_to_json.jsonify(simple_md)
    assert isinstance(json_out, (str,))
    assert "People" in json_out
