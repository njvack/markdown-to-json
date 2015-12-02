#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from HTMLParser import HTMLParser
from collections import deque
import logging
logging.basicConfig(
    level=logging.WARNING,
    format='%(message)s',
    stream=sys.stderr)
logger = logging.getLogger('nester')


class HTMLNode(object):
    def __init__(self):
        self.children = []

    @property
    def is_heading(self):
        return False


class TextNode(HTMLNode):
    def __init__(self, data):
        super(TextNode, self).__init__()
        self.data = data

    def __str__(self):
        return self.data


class ElementNode(HTMLNode):
    def __init__(self, tag, attrs):
        super(ElementNode, self).__init__()
        self.tag = tag
        self.attrs = attrs
        self.attr_dict = dict(attrs)

    def add_data(self, data):
        pass

    @property
    def is_list(self):
        return self.tag in self.LIST_TAGS

    def is_void(self):
        return self.tag in self.VOID_ELEMENTS

    def add_child(self, node):
        self.children.append(node)

    def __str__(self):
        if self.is_void():
            return self.render_void()
        else:
            return self.render_content()

    def render_attrs(self):
        if len(self.attrs) == 0:
            return ""
        return " " + " ".join(
            ['{0}="{1}"'.format(name, val)
                for name, val in self.attrs])

    def render_void(self):
        return "<{0} {1} />".format(self.tag, self.render_attrs())

    def render_content(self):
        return "<{0}{1}>{2}</{0}>".format(
            self.tag, self.render_attrs(),
            "\n".join(str(c) for c in self.children))

    HEADING_TAGS = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}

    LIST_TAGS = {'ol', 'ul'}

    VOID_ELEMENTS = set([
        'area',
        'base',
        'br',
        'col',
        'command',
        'embed',
        'hr',
        'img',
        'input',
        'keygen',
        'link',
        'meta',
        'param',
        'source',
        'track',
        'wbr']
    )


class SimplifiedBodyTreeParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.root = None
        self.working_nodes = deque()

    @property
    def current_element(self):
        if len(self.working_nodes) == 0:
            return None
        return self.working_nodes[-1]

    def handle_starttag(self, tag, attrs):
        if tag == 'body':
            self.root = ElementNode(tag, attrs)
            self.working_nodes.append(self.root)
            return
        if self.current_element is None:
            return
        elt = ElementNode(tag, attrs)
        self.current_element.add_child(elt)
        self.working_nodes.append(elt)

    def handle_endtag(self, tag):
        if self.current_element is None:
            return
        self.working_nodes.pop()

    def handle_data(self, data):
        if self.current_element is None:
            return
        cleaned = data.strip()
        if len(cleaned) == 0:
            return
        text = TextNode(cleaned)
        self.current_element.add_child(text)


def main(file):
    datas = open(file).read()
    nester = Nester()
    nester.feed(datas)


if __name__ == '__main__':
    main(sys.argv[1])
