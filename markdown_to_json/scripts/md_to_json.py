#!/usr/bin/env python
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

from __future__ import print_function, absolute_import, unicode_literals


import sys
from contextlib import contextmanager
import json

import markdown_to_json
from markdown_to_json.vendor.docopt import docopt
from markdown_to_json.vendor import CommonMark

from markdown_to_json.markdown_to_json import Renderer, CMarkASTNester

import logging
logging.basicConfig(
    format="%(message)s", stream=sys.stderr, level=logging.INFO)


@contextmanager
def writable_io_or_stdout(filename):
    if filename is None:
        yield sys.stdout
        return
    else:
        try:
            f = open(filename, 'w')
            yield f
            f.close()
        except:
            logging.error("Error: Can't open {0} for writing".format(
                filename))
            sys.exit(1)


def get_markdown_ast(markdown_file):
    try:
        f = open(markdown_file, 'r')
        return CommonMark.DocParser().parse(f.read())
    except:
        logging.error("Error: Can't open {0} for reading".format(
            markdown_file))
        sys.exit(1)
    finally:
        f.close()


def jsonify_markdown(markdown_file, outfile, indent):
    nester = CMarkASTNester()
    renderer = Renderer()
    with writable_io_or_stdout(outfile) as f:
        ast = get_markdown_ast(markdown_file)
        nested = nester.nest(ast)
        rendered = renderer.stringify_dict(nested)
        json.dump(rendered, f, indent=indent)
        f.write("\n")
    return 0


def main(args=[]):
    pargs = docopt(
        __doc__,
        version="md_to_json {0}".format(markdown_to_json.__version__,),)
    indent = -1
    try:
        indent = int(pargs.get('-i'))
    except:
        logging.error("Error: Indent must be a number")
        sys.exit(1)
    if indent < 0:
        indent = None
    return jsonify_markdown(
        pargs['<markdown_file>'],
        pargs.get('-o'),
        indent)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
