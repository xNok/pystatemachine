"""
CLI Utils

Usage:
  utility_name <path> [-a][-b][-c <option_argument>][--long-d=<argument>]
  utility_name (-h | --help)
  utility_name --version

Options:
    -a                    flag, ie single letters argument
    -b --long-b           flag and long-named options
    -c <option_argument>  flag with option
    --long-d=<argument>   long-named options with argument [default: 10]

Other-Options:
    -h --help                  Show the help message.
    --version                  Show version.
"""
from docopt import docopt


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Utility 20.0')
    print(arguments)