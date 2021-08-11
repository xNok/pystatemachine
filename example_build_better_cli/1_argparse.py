import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('--agg', default="sum",
                    help='aggreagtion function (default: sum)')

args = parser.parse_args()
print(args)