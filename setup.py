#!/usr/bin/env python
# coding: utf-8

import os
import sys

from setuptools import setup

# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()

requires = [
    'gitpython',
    'click'
]

setup(
    name='pipver',
    install_requires=requires,
    scripts=['scripts/pipenv'],
)
