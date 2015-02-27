#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='environment_tools',
    version='0.0.0',
    description='Info about the yelp environments',
    packages=['environment_tools'],
    setup_requires=['setuptools'],
    install_requires=[
        'PyYAML >= 3.10',
    ],
    entry_points={
        'console_scripts': []
    },
    license='Copyright Yelp 2015, All Rights Reserved'
)
