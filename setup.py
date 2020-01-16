#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='python_',
      version='1.0.0',
      description='General state machine implementation in python',
      author='xNok',
      author_email='nokwebspace@gmail.com',
      packages=find_packages(exclude=['docs', 'tests*']),
      entry_points = {
        'console_scripts': [
            'cpm=cli_cpm.cli:main'
        ],
      }
    )