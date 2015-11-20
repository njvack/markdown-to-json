#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nest import TextNode, ElementNode
import sys
import string
import re

import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(message)s',
    stream=sys.stderr)
logger = logging.getLogger('node_formatters')


class SimpleFormatter(object):
    def __init__(self):
        super(SimpleFormatter, self).__init__()

    def format(self, node):
        method = self.TYPE_FORMATTERS.get(type(node))
        if method:
            return method(self, node)
        return ""

    def _format_text_node(self, node):
        logger.debug("_format_text_node")
        return node.data

    def _format_element_node(self, node):
        logger.debug("_format_element_node")
        method = self._format_block_element
        if node.tag in self.INLINE_ELEMENTS:
            method = self._format_inline_element
        formatter_name = "_format_{0}_element".format(node.tag)
        if hasattr(self, formatter_name):
            method = getattr(self, formatter_name)
        logger.debug(formatter_name)
        return method(node)

    def _format_inline_element(self, node):
        return "".join([self.format(c) for c in node.children])

    def _format_strong_element(self, node):
        return "**" + self._format_inline_element(node) + "**"

    def _format_em_element(self, node):
        return "*" + self._format_inline_element(node) + "*"

    def _format_ol_element(self, node):
        return self._format_inline_element(node)

    def _format_ul_element(self, node):
        return self._format_inline_element(node)

    def _format_a_element(self, node):
        if 'href' not in node.attr_dict:
            return self._format_inline_element(node)
        return " [{0}]({1}) ".format(
            self._format_inline_element(node),
            node.attr_dict['href'])

    def _format_block_element(self, node):
        return self._format_inline_element(node) + "\n"

    def _format_li_element(self, node):
        return "* " + self._format_block_element(node)

    def _format_p_element(self, node):
        return self._format_block_element(node) + "\n"

    TYPE_FORMATTERS = {
        TextNode: _format_text_node,
        ElementNode: _format_element_node
    }

    INLINE_ELEMENTS = {
        'b', 'big', 'i', 'small', 'tt', 'abbr', 'acronym', 'cite', 'code',
        'dfn', 'em', 'kbd', 'strong', 'samp', 'time', 'var' 'a', 'bdo', 'br',
        'img', 'map', 'object', 'q', 'script', 'span', 'sub', 'sup', 'button',
        'input', 'label', 'select', 'textarea'
    }


class HeaderKeyFormatter(SimpleFormatter):
    def __init__(self):
        super(HeaderKeyFormatter, self).__init__()

    WS = re.compile('\s+')

    def _format_heading_as_key(self, node):
        contents = self._format_inline_element(node)
        capitalized = string.capwords(contents)
        return self.WS.sub('', capitalized) + "\n"

    _format_h1_element = _format_heading_as_key
    _format_h2_element = _format_heading_as_key
    _format_h3_element = _format_heading_as_key
    _format_h4_element = _format_heading_as_key
    _format_h5_element = _format_heading_as_key
    _format_h6_element = _format_heading_as_key
