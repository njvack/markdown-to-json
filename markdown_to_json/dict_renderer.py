#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from functools import reduce
import operator
from .vendor.ordereddict import OrderedDict


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
