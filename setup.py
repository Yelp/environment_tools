#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='environment_tools',
    version='1.0.1',
    description='Utilities for describing Yelp hardware environments',
    packages=['environment_tools'],
    setup_requires=['setuptools'],
    install_requires=[
        'argparse >= 1.3.0',
        'simplejson >= 2.1.0',
        'networkx >= 1.9.1',
    ],
    entry_points={
        'console_scripts': []
    },
    license='Copyright Yelp 2015, All Rights Reserved',
    include_package_data=True
)
