#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Part of the markdown_to_json package
# Written by Nate Vack <njvack@freshforever.net>
# Copyright 2015 Board of Regents of the University of Wisconsin System

from __future__ import unicode_literals, absolute_import

from functools import reduce
import operator

from .vendor.ordereddict import OrderedDict

"""
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


class CMarkASTNester(object):
    def __init__(self):
        super(CMarkASTNester, self).__init__()

    def nest(self, ast):
        return self._dictify_blocks(ast.children, 1)

    def _dictify_blocks(self, blocks, heading_level):
        def matches_heading(block):
            return block.t == 'ATXHeader' and block.level == heading_level

        if not any((matches_heading(b) for b in blocks)):
            self._ensure_list_singleton(blocks)
            return blocks

        splitted = dictify_list_by(blocks, matches_heading)
        for heading, nests in splitted.items():
            splitted[heading] = self._dictify_blocks(nests, heading_level + 1)
        return splitted

    def _ensure_list_singleton(self, blocks):
        lists = [e for e in blocks if e.t == 'List']
        if len(blocks) > 1 and len(lists) > 0:
            l = lists[0]
            raise ContentError(
                "Error at line {0}: Can't mix lists and other content".format(
                    l.start_line))


class ContentError(ValueError):
    pass


def dictify_list_by(l, fx):
    result = OrderedDict()
    cur = None
    children = []
    for item in l:
        if fx(item):
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


class Renderer(object):
    def __init__(self):
        super(Renderer, self).__init__()

    def stringify_dict(self, d):
        out = OrderedDict(
            [
                (self._render_block(k), self._valuify(v))
                for k, v in d.items()
            ])
        return out

    def _valuify(self, cm_vals):
        if hasattr(cm_vals, 'items'):
            return self.stringify_dict(cm_vals)
        if len(cm_vals) == 0:
            return ''
        first = cm_vals[0]
        if first.t == 'List':
            return self._render_List(first)
        return "\n\n".join([self._render_block(v) for v in cm_vals])

    def _render_block(self, block):
        method_name = "_render_{0}".format(block.t)
        method = self._render_generic_block
        if hasattr(self, method_name):
            method = getattr(self, method_name)
        return method(block)

    def _render_generic_block(self, block):
        if hasattr(block, 'strings') and len(block.strings) > 0:
            return "\n".join(block.strings)
        if len(block.children) > 0:
            return [self._render_block(b) for b in block.children]

    def _render_List(self, block):
        # We need to de-nest this one level -- we'll use the trick that
        # lists can be added to do this.
        list_items = [self._render_block(li) for li in block.children]
        return reduce(operator.add, list_items)

    def _render_FencedCode(self, block):
        return "```\n" + block.string_content + "```"
