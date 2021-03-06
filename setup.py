#!/usr/bin/env python
# -*- coding: utf-8 -*-

# © 2015-2018, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

import re
import os
import codecs
from setuptools import setup, find_packages

with open('./pytest_score/__init__.py', 'r') as f:
    MATCH_EXPR = "__version__[^'\"]+(['\"])([^'\"]+)"
    VERSION = re.search(MATCH_EXPR, f.read()).group(2).strip()


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-score',
    version=VERSION,
    author='Dominik Gresch',
    author_email='greschd@gmx.ch',
    maintainer='Dominik Gresch',
    maintainer_email='greschd@gmx.ch',
    license='Apache 2.0',
    url='https://github.com/greschd/pytest-score',
    description='A plugin to run quality (non-binary) tests with pytest.',
    long_description=read('README.md'),
    packages=find_packages(),
    include_package_data=True,
    package_data={'pytest_score': ['templates/*']},
    python_requires='>=3.5',
    install_requires=['pytest>=3.1.1', 'fsc.export', 'py', 'jinja2', 'numpy'],
    extras_require={
        'dev':
        ['sphinx', 'pylint==2.1.1', 'yapf==0.25.0', 'prospector==1.1.6.2'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
    ],
    entry_points={
        'pytest11': [
            'score = pytest_score',
        ],
    },
)
