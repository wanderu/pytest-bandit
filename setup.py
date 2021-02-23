#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup, find_packages
from pytest_bandit import __version__


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-bandit',
    version=__version__,
    author='Wanderu',
    author_email='oss@wanderu.com',
    maintainer='Matthew Warren',
    maintainer_email='mwarren@wanderu.com',
    license='MIT',
    url='https://github.com/Wanderu/pytest-bandit',
    description='A bandit plugin for pytest',
    long_description=read('README.rst'),
    packages=find_packages(exclude=['tests']),
    python_requires='~=3.4',
    install_requires=[
        'pytest>=3.5.0',
        'bandit>=1.4.0'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'bandit = pytest_bandit.plugin',
        ],
    },
)
