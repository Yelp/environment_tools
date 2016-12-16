#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

from environment_tools import version

setup(
    name='environment_tools',
    version=version,
    description='Utilities for working with hierarchical environments',
    packages=['environment_tools'],
    install_requires=['networkx >= 1.9.1'],
    license='Copyright Yelp 2015, All Rights Reserved',
)
