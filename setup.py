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
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows :: Windows 10'
    ],
    package_data={'eurovision/data/': ['eurovision/data/countries-2016.csv']},
    include_package_data=True,
)
