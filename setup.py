#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

VERSION = '0.0.0'

setup(
    name='pyusergrid',
    version=VERSION,
    description='Python Usergrid Client',
    author='BennEic',
    author_email='benn@eichhorn.co',
    url='https://github.com/beichhor/python-usergrid-client',
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=[
        'requests>=1.0',
        'simplejson>=3.1',
    ],
    setup_requires=[
        'nose',
    ],
)
