from setuptools import setup

setup(
    name='fancy_agg',
    entry_points={
        'aggregators': [
            'fancy = fancy:main',
        ],
    }
)