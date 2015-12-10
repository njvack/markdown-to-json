#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages, Command
import os

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
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)


def get_locals(filename):
    l = {}
    exec(open(filename, 'r').read(), {}, l)
    return l

metadata = get_locals(os.path.join('markdown_to_json', '_metadata.py'))

setup(
    name="markdown-to-json",
    version=metadata['version'],
    author=metadata['author'],
    author_email=metadata['author_email'],
    license=metadata['license'],
    url=metadata['url'],
    packages=find_packages(),
    cmdclass={'test': PyTest},
    entry_points={
        'console_scripts': [
            'md_to_json = markdown_to_json.scripts.md_to_json:main'
        ]}
    )
