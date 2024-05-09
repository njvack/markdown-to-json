"""
Utilities
"""

import os


def locate_file(file_name: str, executing_file: str) -> str:
    """
    Find file relative to a source file, e.g.
    locate("foo/bar.txt", __file__)

    Succeeds regardless to context of execution

    File must exist
    """
    file_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(executing_file)), file_name))
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    return file_path
