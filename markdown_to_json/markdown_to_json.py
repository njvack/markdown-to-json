"""
Part of the markdown_to_json package
Written by Nate Vack <njvack@freshforever.net>
Copyright 2023 Board of Regents of the University of Wisconsin System

This module contains a class to change a CommonMark.py AST into a nested
OrderedDict structure. Its rules:

* Headings are keys. Stuff following headings are values.
* Values are generally treated as strings, and left unchanged; in other words
  you'll generally get the markdown.
* The exception is lists -- they're turned into arrays.
* Lists must occur alone after a heading.
* You can nest lists; you'll get nested arrays.
* To increase key nesting level, use higher-numbered headers. You can't go
  past 6. That would be insane anyhow.
* You'll want to monotonically increasing heading numbers (eg, a H1 followed
  by a H2) -- if you jump, it's valid but the high-numbered headings won't be
  treated as keys.
* Content ordering is unchanged.

To use:

md = \"""
# First Heading

Foo bar baz corge

# Second Heading

* List 1
* List 2
\"""

ast = CommonMark.DocParser().parse(md)
nested = CMarkASTNester().nest(ast)

Note that you'll want to turn the nested structure into a string.

In addition, this module contains a Renderer class; this transforms the nested
structure from CMarkASTNester into an OrderedDict with strings as keys and
strings, lists, or OrderedDicts as values.
"""

from __future__ import absolute_import, unicode_literals

import json
import operator
from collections import OrderedDict
from functools import reduce
from typing import Any, Dict, List, Optional, Union

from .vendor import CommonMark
from .vendor.CommonMark.CommonMark import Block


def dictify(markdown_str: str):
    """
    Turn a markdown string into a nested python dict
    Really, just a little semantic sugar
    """
    ast = CommonMark.DocParser().parse(markdown_str)
    nested = CMarkASTNester().nest(ast)
    return Renderer().stringify_dict(nested)


def jsonify(markdown_str: str):
    """
    Turn a markdown string into a json string
    Also just semantic sugar
    """
    d = dictify(markdown_str)
    return json.dumps(d)


class CMarkASTNester:
    """Nests DOM into a python dictionary"""

    # def __init__(self):
    #     super(CMarkASTNester, self).__init__()

    def nest(self, ast: Block):
        """Outermost next call"""

        # Handle documents with ## as the top ATX header.
        parts = [block.level if hasattr(block, "level") else 100000 for block in ast.children]
        if parts:
            minimum = min(parts)
            return self._dictify_blocks(ast.children, minimum)
        return []

    def _dictify_blocks(self, blocks: Block, heading_level: int):
        """Recursive nest call"""

        def matches_heading(block):
            """Filter function to match headers"""
            return block.t == "ATXHeader" and block.level == heading_level

        if not any((matches_heading(b) for b in blocks)):
            self._ensure_list_singleton(blocks)
            return blocks

        splitted = dictify_list_by(blocks, matches_heading)
        for heading, nests in splitted.items():
            splitted[heading] = self._dictify_blocks(nests, heading_level + 1)
        return splitted

    def _ensure_list_singleton(self, blocks):
        """Make sure lists don't mix content"""


class ContentError(ValueError):
    """Content Error"""


def dictify_list_by(list_of_blocks: List[Any], filter_function) -> Dict[Any, Any]:
    """Turn list of tokens into dictionary of lists of tokens."""
    result = OrderedDict()
    cur = None
    children: list[Any] = []
    for item in list_of_blocks:
        if filter_function(item):
            if cur:
                # Pop cur, children into result
                result[cur] = children
            cur = item
            children = []
            continue
        children.append(item)
    if cur:
        result[cur] = children
    return result


class Renderer:
    """Processes DOM"""

    # def __init__(self):
    #     super(Renderer, self).__init__()

    def stringify_dict(self, dictionary: Dict[Any, Any]) -> OrderedDict:
        """Create dictionary of keys and values as strings"""
        if isinstance(dictionary, dict):
            out = OrderedDict([(self._render_block(k), self._valuify(v)) for k, v in dictionary.items()])
        else:
            out = OrderedDict([("root", [self._render_block(v) for v in dictionary])])
        return out

    def _valuify(self, cm_vals: Any) -> Any:
        """Render values of dictionary as scalars or lists"""
        if hasattr(cm_vals, "items"):
            return self.stringify_dict(cm_vals)
        if len(cm_vals) == 0:
            return ""
        first = cm_vals[0]
        if first.t == "List":
            return self._render_List(first)
        # HACK: This is just str'ing the unexpected lists
        return "\n\n".join([str(self._render_block(v)) for v in cm_vals])

    def _render_block(self, block: Block):
        """Render any block"""
        method_name = "_render_{0}".format(block.t)
        method = self._render_generic_block
        if hasattr(self, method_name):
            method = getattr(self, method_name)
        return method(block)

    # function name called based on block type
    # pylint: disable=invalid-name
    def _render_generic_block(self, block: Block) -> Optional[Union[str, List[Any]]]:
        """Render any block"""
        if hasattr(block, "strings") and hasattr(block.strings, "__len__") and len(block.strings) > 0:
            return "\n".join(item.decode("utf8") if isinstance(item, bytes) else item for item in block.strings)
        if len(block.children) > 0:
            return [self._render_block(b) for b in block.children]
        # Is this an error state?
        return []

    # function name called based on block type
    # pylint: disable=invalid-name
    def _render_List(self, block: Block):
        """Render list"""
        # We need to de-nest this one level -- we'll use the trick that
        # lists can be added to do this.
        list_items = [self._render_block(li) for li in block.children]
        return reduce(operator.add, list_items)

    # function name called based on block type
    # pylint: disable=invalid-name
    def _render_FencedCode(self, block: Block) -> str:
        """Render code"""
        return "```\n" + block.string_content + "```"
