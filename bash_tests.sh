set -e
python -m markdown_to_json.scripts.md_to_json -h
python -m markdown_to_json.scripts.md_to_json examples/list.md
python -m markdown_to_json.scripts.md_to_json examples/same.md
python -m markdown_to_json.scripts.md_to_json examples/simple.md
python -m markdown_to_json.scripts.md_to_json examples/complicated.md
python -m markdown_to_json.scripts.md_to_json
