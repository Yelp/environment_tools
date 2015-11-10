#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

from environment_tools import version

setup(
    name='environment_tools',
    version=version,
    description='Utilities for working with hierarchical environments',
    packages=['environment_tools'],
    setup_requires=['setuptools'],
    install_requires=[
        'argparse >= 1.2.1',
        'simplejson >= 2.1.0',
        'networkx == 1.9.1',
    ],
    entry_points={
        'console_scripts': []
    },
    license='Copyright Yelp 2015, All Rights Reserved',
    include_package_data=True
)
