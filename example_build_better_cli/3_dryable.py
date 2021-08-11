"""
Process some integers.

usage: 3_dryable.py [-h] [--dry-run] FILE [FILE ...] 

positional arguments:
  FILE           a path to a file you want to delete

optional arguments:
  -h, --help  show this help message and exit
  --dry-run   will not delete you file
"""
from docopt import docopt
import dryable

arguments = docopt(__doc__, version='Utility 20.0')
print(arguments)

dryable.set(arguments['--dry-run'])

@dryable.Dryable()
def deleteFiles( files: list):
    print( 'This will delete your files forever')

deleteFiles( arguments['FILE'] )