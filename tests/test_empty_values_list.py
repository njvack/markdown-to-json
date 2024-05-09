import markdown_to_json


def test_empty_values():
    value = """- a
-
- b
-"""
    stringified = markdown_to_json.jsonify(value)
    assert stringified == '{"root": [["a", "b"]]}'
