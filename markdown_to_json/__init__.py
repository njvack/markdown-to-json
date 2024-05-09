"""
markdown-to-json
"""

from __future__ import absolute_import

from ._metadata import author as __author__
from ._metadata import version as __version__
from .markdown_to_json import dictify, jsonify

__all__ = ["__author__", "__version__", "dictify", "jsonify"]
