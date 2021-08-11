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

import os, json

def main():

  cli_arguments = docopt(__doc__, version='Utility 20.0')

  # Implement rc file
  rc_file_name = ".foorc"
  rc_arguments = {}
  if os.path.exists(rc_file_name):
      print(f"Loading runtime config from {rc_file_name} file")
      with open(rc_file_name) as f:
          rc_arguments = json.load(f)
  else:
      print(f"Locally you can use {rc_file_name} file to avoide typing all flags and arguments every time")
      print(f"Simply copy the following config to {rc_file_name} to get started")
      print(cli_arguments)

  arguments = {**cli_arguments, **rc_arguments}
  print(arguments)