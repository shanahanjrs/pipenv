#!/usr/bin/env python
# coding: utf-8

import os
import sys

from setuptools import setup

requires = [
    'gitpython',
    'click'
]

setup(
    name='pipver',
    version='0.1.6',
    description='Python package versioning the right way.',
    author='John Shanahan',
    author_email='shanahan.jrs@gmail.com',
    url='https://github.com/shanahanjrs/pipver',
    include_package_data=True,
    install_requires=requires,
    scripts=['scripts/pipver'],
)
