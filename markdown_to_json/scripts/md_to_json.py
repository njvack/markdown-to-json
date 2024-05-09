#!/usr/bin/env python
# Part of the markdown_to_json package
# Written by Nate Vack <njvack@freshforever.net>
# Copyright 2023 Board of Regents of the University of Wisconsin System
"""Translate markdown into JSON.

Usage:
  md_to_json [options] <markdown_file>
  md_to_json -h | --help

Options:
  -h --help     Show this screen
  --version     Print version number
  -o <file>     Save output to a file instead of stdout
  -i <val>      Indent nested JSON by this amount. Use a negative number for
                most compact possible JSON. the [default: 2]
"""

from __future__ import absolute_import, print_function, unicode_literals

import json
import logging
import sys
from contextlib import contextmanager
from typing import Optional

import markdown_to_json
from markdown_to_json.markdown_to_json import CMarkASTNester, Renderer
from markdown_to_json.vendor import CommonMark
from markdown_to_json.vendor.docopt import docopt

logging.basicConfig(format="%(message)s", stream=sys.stderr, level=logging.INFO)


@contextmanager
def writable_io_or_stdout(filename: Optional[str]):
    """Switch between file and stdout"""
    if filename is None:
        yield sys.stdout
        return

    try:
        file = open(filename, "w", encoding="utf8")
        yield file
        file.close()
    # pylint: disable=bare-except
    except Exception as ex:
        logging.error(f"Error: Can't open {filename} for writing, {ex}")
        sys.exit(1)


def get_markdown_ast(markdown_file: str):
    """Parse AST"""
    # pylint: disable=bare-except
    with open(markdown_file, "r", encoding="utf8") as file:
        try:
            return CommonMark.DocParser().parse(file.read())
        except:
            logging.error("Error: Can't open {0} for reading".format(markdown_file))
            sys.exit(1)


def jsonify_markdown(markdown_file: str, outfile: Optional[str], indent: int) -> int:
    """Jsonify the markdown"""
    nester = CMarkASTNester()
    renderer = Renderer()
    with writable_io_or_stdout(outfile) as file:
        ast = get_markdown_ast(markdown_file)
        nested = nester.nest(ast)
        rendered = renderer.stringify_dict(nested)
        json.dump(rendered, file, indent=indent, ensure_ascii=False)
        file.write("\n")
    return 0


def main():
    pargs = docopt(
        __doc__,
        version="md_to_json {0}".format(
            markdown_to_json.__version__,
        ),
    )
    # indent = -1

    try:
        indent = int(pargs.get("-i"))
    # pylint: disable=bare-except
    except:
        logging.error("Error: Indent must be a number")
        sys.exit(1)
    if indent < 0:
        indent = None
    return jsonify_markdown(pargs["<markdown_file>"], pargs.get("-o"), indent)


if __name__ == "__main__":
    sys.exit(main())
