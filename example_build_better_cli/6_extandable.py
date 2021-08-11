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
import pkg_resources

import os, json

def get_aggregators():
    agg = {
        'sum': sum,
        'max': max,
    }
    for entry_point in pkg_resources.iter_entry_points('aggregators'):
        agg[entry_point.name] = entry_point.load()
    return agg

def aggregate(N: list, agg_name, aggregators):

  if agg_name in aggregators:
    agg = aggregators[agg_name]
    return agg([int(i) for i in N])
  else:
    print(f"Aggregation function {agg_name} is not implemented")
    return 0
  

def main():

  arguments = docopt(__doc__, version='Utility 20.0')

  print(arguments)

  aggregators = get_aggregators()
  print(aggregators)

  result = aggregate(arguments["N"], arguments["--agg"], aggregators)

  print(f"result: {result}")




    
if __name__ == '__main__':
    main()