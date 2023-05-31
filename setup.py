#!/usr/bin/env python

from setuptools import setup, find_packages, Command
import os
from pathlib import Path

packages = find_packages()


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import sys
        import subprocess

        errno = subprocess.call([sys.executable, "runtests.py"])
        raise SystemExit(errno)


def get_locals(filename):
    the_locals = {}
    exec(open(filename, "r").read(), {}, the_locals)
    return the_locals


metadata = get_locals(os.path.join("markdown_to_json", "_metadata.py"))

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="markdown-to-json",
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=metadata["version"],
    author=metadata["author"],
    author_email=metadata["author_email"],
    license=metadata["license"],
    url=metadata["url"],
    packages=find_packages(),
    cmdclass={"test": PyTest},
    entry_points={"console_scripts": ["md_to_json = markdown_to_json.scripts.md_to_json:main"]},
)
