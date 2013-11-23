#!/usr/bin/env python
"""PyPi Configuration File Manager."""
__author__ = 'Joe Petrini <joepetrini__@__gmail__com>'
__copyright__ = 'Copyright 2013 PayrollDeduct, LLC'
__license__ = 'MIT License'
from distutils.core import setup

setup(
    name='Listrak API Wrapper',
    version='0.1dev',
    packages=['listrak-wrapper',],
    license='MIT License',
    long_description=open('README.md').read(),
)