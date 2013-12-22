#!/usr/bin/env python
"""PyPi Configuration File Manager."""
__author__ = 'Joe Petrini <joepetrini__@__gmail__com>'
__copyright__ = 'Copyright 2013 PayrollDeduct, LLC'
__license__ = 'MIT License'
from setuptools import setup

# magic
setup(
    name='Listrak API wrapper',
    version='0.5',
    description='Python library accessing the Listrak SOAP api',
    long_description=open('README.md').read(),
    author='Joe Petrini',
    author_email='joepetrini@gmail.com',
    url='https://github.com/joepetrini/python-listrak',
    download_url='https://github.com/joepetrini/python-listrak/archive/master.zip#egg=listrak-wrapper',
    license='MIT License',
    install_requires=['xmltodict','requests'],
    py_modules=['listrak-wrapper'],
    platforms=["any"]
)