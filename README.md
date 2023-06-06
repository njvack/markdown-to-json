# Markdown to JSON converter

## Description

A simple tool to convert Markdown (CommonMark dialect) data into JSON. It uses headings as JSON keys, and the stuff following headings as values. Lists are turned into arrays. Higher heading values yield nested JSON keys.

## Is this for me?

If you have to ask that question, it probably isn't. Here are some cases where I'd recommend something else:

### I want to parse arbitrary Markdown

In this case, I'd recommend the excellent [markdown-it-py](https://github.com/executablebooks/markdown-it-py)

### I want to hand-write nested structures but hate writing JSON by hand

In this case, [TOML](https://toml.io/en/) might be what you're looking for. [Python support is built-in as of 3.11](https://docs.python.org/3/library/tomllib.html). If I had known of TOML, I would never have written this package.

### Nope, those situations don't cover me; I really want to parse Markdown into data

If you don't mind the loss of fidelity to the exact Markdown Document Object Model (DOM), you can get a simple python or json data structure to extract data-like structures from a subset of Markdown documents.

This tool was built to allow easier creation of dataset descriptions for the [Brain Imaging Data Structure](http://bids.neuroimaging.io/) data sharing specification.

## Installation

Non isolated install from pypi
```bash
pip install markdown-to-json
md_to_json --help
```

Isolated install with pipx if you only want the CLI
```bash
pipx install markdown-to-json
md_to_json --help
```

Install bleeding edge from github
```bash
pip install git+https://github.com/njvack/markdown-to-json/
python -m markdown_to_json --help
```

```bash
git clone https://github.com/njvack/markdown-to-json.git
cd markdown_to_json
./setup.py install
```

The package has no external requirements and has been tested python 3.6+.

Please use version 1 or 1.1 for python 2.x.

## CLI Usage, `md_to_json`

```
Translate Markdown into JSON.

Usage:
  md_to_json [options] <markdown_file>
  md_to_json -h | --help

Options:
  -h --help     Show this screen
  --version     Print version number
  -o <file>     Save output to a file instead of stdout
  -i <val>      Indent nested JSON by this amount. Use a negative number for
                most compact possible JSON. the [default: 2]
```

## Programmatic usage
```python
import markdown_to_json
value = """
# Nested List

* Item 1
    * Item 1.1
* Item 2
"""

# The simple way:
dictified = markdown_to_json.dictify(value)
assert dictified == {'Nested List': ['Item 1', ['Item 1.1'], 'Item 2']}

# Or, if you want a json string
jsonified = markdown_to_json.jsonify(value)
assert jsonified == """{"Nested List": ["Item 1", ["Item 1.1"], "Item 2"]}"""
```

This translates a Markdown document into JSON as described in the example below.

## Example

The Markdown:

```markdown
# Description

This is an example file

# Authors

* Nate Vack
* Vendor Packages
    * docopt
    * CommonMark-py

# Versions

## Version 1

Here's something about Version 1; I said "Hooray!"

## Version 2

Here's something about Version 2
```

will translate to the JSON:

```json
{
  "Description": "This is an example file",
  "Authors": ["Nate Vack", "Vendor Packages", ["docopt", "CommonMark-py"]],
  "Versions": {
    "Version 1": "Here's something about Version 1; I said \"Hooray!\"",
    "Version 2": "Here's something about Version 2"
  }
}
```

## Credits

`markdown_to_json` was written by [Nate Vack](https://github.com/njvack) at the Center for Healthy Minds at the University of Wisconsin–Madison.

Maintenance development by [Matthew Martin](https://github.com/matthewdeanmartin/)

This tool ships a few really excellent tools in its `vendor` directory:

[docopt](https://github.com/docopt/docopt) is copyright (c) 2012 Vladimir Keleshev, <vladimir@keleshev.com>

Upgraded to docopt-ng.

[CommonMark-py](https://github.com/rolandshoemaker/CommonMark-py) is copyright Copyright (c) 2014, Bibek Kafle and Roland Shoemaker.

Cannot upgrade to 0.6.0 because of breaking changes in AST.
