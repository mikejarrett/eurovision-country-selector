#!/usr/bin/env python
# -*- coding: utf-8 -*-
from codecs import open
from os import path
from setuptools import setup, find_packages


here = path.abspath(path.dirname(__file__))


with open(path.join(here, 'README.rst'), encoding='utf-8') as file_:
    long_description = file_.read()


setup(
    name="eurovision-country-selector",
    version="1.0.0.2016",
    author='Mike Jarrett',
    author_email='mike<dot>d<dot>jarrett<at>gmail<dot>com',
    description='Select a country for your EuroVision party.',
    long_description=long_description,
    url='https://github.com/mikejarrett/eurovision-country-selector',
    license='MIT',
    packages=find_packages(),
    tests_require=['nose', 'coverage', 'unittest2'],
    entry_points={
        'console_scripts': [
            'eurovision=eurovision.cli:main',
        ],
    }
)
