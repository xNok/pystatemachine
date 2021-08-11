#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='python_better_cli',
      version='1.0.0',
      description='5 tricks to improve command lines',
      author='xNok',
      author_email='xNok@gmail.com',
      packages=find_packages(exclude=['docs', 'tests*']),
      entry_points = {
        'console_scripts': [
            'foobar=5_setup:main'
        ],
      }
    )