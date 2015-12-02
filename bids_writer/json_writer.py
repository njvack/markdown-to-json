#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict
from .node_formatters import JSONPrepFormatter

"""
This module converts an HTML tree structure into an OrderedDict, from whence
it can be trivially made into json. You'll usually use it like:

html = html_text_from_somewhere
parser = parser.SimplifiedBodyTreeParser()
parser.feed(html)
nester = json_writer.TreeNester()
nested = nester.nest(parser.root)
json.dumps(nested)

Its rules:

* Headings define the nesting level of following content
* Headings must start with h1
* The contents of headings are dict keys
* Following content is the dict value
* Headings must all be direct children of the parent node
* Heading level may increment by at most one from the current level -- for
  example, h1+h1 and h1+h2 are OK, but h1+h3 is not.
* Heading level may decrement by more than one. So h2+h1 and h3+h1 are OK.
* Most tags are stripped. <strong>, <em>, and <a> tags may be converted to
  their markdown equivalents.
"""


class TreeNester(object):
    def __init__(self, formatter_factory=JSONPrepFormatter):
        self.formatter = formatter_factory()
        super(TreeNester, self).__init__()

    def jsonify(self, root):
        nested = self.nest(root)
        return self._jsonify_element_dict(nested)

    def _jsonify_element_dict(self, element_dict):
        out = OrderedDict()
        for elem_key, elem_values in element_dict.items():
            key = self.formatter.format(elem_key).strip()
            valueizer = self._valueize_method(elem_values)
            value = valueizer(elem_values)
            out[key] = value
        return out

    def _valueize_method(self, value):
        if hasattr(value, 'items'):
            return self._jsonify_element_dict
        if len(value) == 1:
            first = value[0]
            if first.is_list:
                return self._valueize_list
        return self._valueize_text

    def _valueize_list(self, l):
        return [self.formatter.format(v) for v in l]

    def _valueize_text(self, l):
        return "\n\n".join([self.formatter.format(v) for v in l]).strip()

    def nest(self, root):
        return self.split_elements(root.children, 1)

    def split_elements(self, element_list, heading_level):
        def matches_heading(element):
            return element.tag == "h" + str(heading_level)
        if not any((matches_heading(item) for item in element_list)):
            return element_list
        splitted = dictify_list_by(element_list, matches_heading)
        for heading, nests in splitted.items():
            splitted[heading] = self.split_elements(nests, heading_level + 1)
        return splitted

    def _ensure_list_singleton(self, element_list):
        if len(element_list) > 1 and any((e.is_list for e in element_list)):
            raise ValueError("Can't mix lists and other stuff")


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
