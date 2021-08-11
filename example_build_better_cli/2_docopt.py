"""
Process some integers.

usage: 2_docopt.py [-h] [--agg AGG] N [N ...] 

positional arguments:
  N           an integer for the accumulator

optional arguments:
  -h, --help  show this help message and exit
  --agg AGG   aggregation function [default: sum]
"""
from docopt import docopt

arguments = docopt(__doc__, version='Utility 20.0')
print(arguments)
