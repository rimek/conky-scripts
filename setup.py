#!/usr/bin/env python

import os
from setuptools import setup, find_packages
#from DistUtilsExtra.command import build_icons 


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

NAME = 'conky-scripts'
VERSION = read('VERSION').replace("\n",'')
DESCRIPTION = read('README.rst')

setup(
    name = NAME,
    version = VERSION,
    description = 'Conky scripts',
    author = 'Marcin Rim',
    author_email = 'rimek@rimek.org',
    packages = find_packages(),
    long_description = DESCRIPTION, 
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    keywords = 'system',
    license = 'BSD',
    install_requires = [
        'imaplib2',
        'setuptools',
        'keyring',
        'setproctitle',
    ],
    zip_safe = False,
    entry_points = {
        'console_scripts': [
           'conky-scripts = conky_scripts.main:run',
        ],
    },
)
