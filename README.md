# Markdown to JSON converter

## Description

A simple tool to convert Markdown (technically CommonMark) data into JSON. It uses headings as JSON keys, and the stuff following headings as values. Lists are turned into arrays. Higher heading values yield nested JSON keys.

## Why the hell would I want to do this?

Sometimes, you need to write JSON. Writing it by hand is a pain. It's a fiddly format and there are strings to escape and commas and it looks bad and you'll have validation errors and yuck. You could build a custom tool to write your particular JSON, but that's a bunch of work. You could use some JSON-specific editor, but they tend to be pretty neckbeard. Sometimes, you maybe just want to open a text editor and pump out a little nested data structure in a human-readable way.

This lets you do that. Markdown is easy.

As a point of reference, this tool was built to allow easy(-ish) creation of dataset descriptions for the [Brain Imaging Data Structure](http://bids.neuroimaging.io/) data sharing specification.

## Installation

Easy method:

```
pip install markdown-to-json
```

Also easy method:

```
git clone https://github.com/njvack/markdown-to-json.git
cd markdown_to_json
./setup.py install
```

The package has no external requirements and has been tested on python 2.6.6 through 3.4.3.

You'll get one executable:

## `md_to_json`

```
Translate markdown into JSON.

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

This translates a markdown document into JSON as described in the example below.

## Example

The markdown:

```
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

```
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

`markdown_to_json` was written by Nate Vack <njvack@freshforever.net> at the Center for Healthy Minds at the University of Wisconsin–Madison.

This tool ships a few really excellent tools in its `vendor` directory:

[docopt](https://github.com/docopt/docopt) is copyright (c) 2012 Vladimir Keleshev, <vladimir@keleshev.com>

[CommonMark-py](https://github.com/rolandshoemaker/CommonMark-py) is copyright Copyright (c) 2014, Bibek Kafle and Roland Shoemaker

The packaged ordereddict implementation is copyright (c) 2009 Raymond Hettinger