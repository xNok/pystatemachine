# 5 Tips to to Create Better Command Line Interface

One very common usage of Python is to create toobox, to help you complete repeatable task. If you are reading this article I am sure that you when throuth the process of creating a automation script in Python. At some point, you started refactoring your script to make it a proper command line tool. Adding argument, configuration, prompt and instructions.

Since it is such a commun task. I decided to compile and share my best trick I try to add to my command line whenever I create one.

## 1 Choose the right tool to parse your arguments

This first upgrade to an automation script is to add arguments to pass values to your program and make it customizable.

One thing is certain I hate to use the native [argparse](https://docs.python.org/3/library/argparse.html) package. This packages is extremely verbose, meaning that it requires a lot of code to simple achieve tasks. Here is a simple example from the documentation of [argparse](https://docs.python.org/3/library/argparse.html) for reference:

```
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

args = parser.parse_args()
print(args)
```

The way we pass argument as become standardized with the [POSIX utility conventions](https://pubs.opengroup.org/onlinepubs/009695399/basedefs/xbd_chap12.html) and [GNU extension](https://www.gnu.org/prep/standards/html_node/Command_002dLine-Interfaces.html). Since parsing argument is based on a convention, we can find Python package to help you write better and smarter command line interfaces. All have their stength and weakness. But in my opinion the best of all is [docopt](http://docopt.org/). Docopt forces you to focus on the documentation and magically parse all arguments for you. Lets write the same example using Docopt:


```
"""
Process some integers.

usage: 2_docopt.py [-h] [--sum] N [N ...] 

positional arguments:
  N           an integer for the accumulator

optional arguments:
  -h, --help  show this help message and exit
  --sum       sum the integers (default: find the max)
"""
from docopt import docopt

arguments = docopt(__doc__, version='Utility 20.0')
print(arguments)
```

Did you notice? All that we really did is to write the documentation for our command line and docopt handles the rest. this one liner does the tick:

```
arguments = docopt(__doc__, version='Utility 20.0')
```

Docopt takes as a input the docstrings (__doc__) of your file and the command you invoqued and return a dictionnary with all the flags and positional arguments.

```
{'--help': False,
 '--sum': False,
 'N': ['test']}
```

## 2 Implement a dry run

Often when creating a CLI for automation you wish you could know what action you CLI will do without impacting any thing.

In that case you are tempted to write a simple dry-run mecanism that lets you run the command line but skipt all impacting changes, such as http call to APIs. Lucky for you [dryable](https://github.com/haarcuba/dryable) is a simple Python packages makes the implementation simple thanks to a the clever use of [decorator](https://realpython.com/primer-on-python-decorators/).

```
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
```

As you can see I reused docopt in this example as well. It is easy to add a new argument `--dry-run` that will be reflected in the dict `arguments` that hold all arguments once parsed by docopt. We use `dryable.set(arguments['--dry-run'])` to activate or not dryable base on the presence of the flag `--dry-run`. If dryable is activated then every function decorated with `@dryable.Dryable()` will be skipt. 

## 3 Creating a .rc file

Once you reach a certain complexity in your command line, defining everytime all arguments can become very teadious.

You may already be familiar with `.rc` files such as `.npmrc`, `.bashrc`. `.vimrc`. Those files are configuration files for a specific command line interface. There name is codified; it start with `.`, then the name of the CLI followed by `rc`. If we refer to wikipedia to get a proper definition we get:

> In the context of Unix-like systems, the term rc stands for the phrase "run commands". It is used for any file that contains startup information for a command.

Supporting a `rc` file in your CLI makes it easy to share configuration alongside a project via commiting that file to your repository. It also prevent user from repeating arguments they often use. This steamline the use of a command line. 

By using docopt, creating an `.rc` file is easy. Simple takes the resulting dict called `arguments` in our example, save it to a file. There you go you have an `.rc` file. Now all you need to do is to check if that file exist whenever the command is invoques and merged its content with `arguments`. Here is an example:

```python
"""
Process some integers.

usage: 2_docopt.py [-h] [--sum] N [N ...] 

positional arguments:
  N           an integer for the accumulator

optional arguments:
  -h, --help  show this help message and exit
  --sum       sum the integers (default: find the max)
"""
from docopt import docopt

import os, json

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
```

In our previous example you had to include `--sum` all the time for the command to work.

```
python .\2_docopt.py 2 3 --sum
```

What if you know that you only want to use the `--sum` and are tired of repeating yourself. Well it is easy know with our rc file called `.foorc`. Add the following content to `.foorc`

```
{
  "--sum": true
}
```

Now you are free from the run the command line without `--sum`

```
python .\4_rc_file.py 2 3
```

## 4 Installing the Command Line

Once you command line script start to look like something other user would use. You probaly want to make it installable.

This is that base when creating a command line you want to share. It will be added to the PATH so you can call it directly without invoquing the python script. Intalling the command line happend during the setup phase when using pip.

The following `setup.py` will install the cli

```
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
```

The most important part for this to work in the `entry_point` attribute.

```
'console_scripts': [
    'foobar=5_setup:main'
],
```

This tels python to register a console script called `foobar` that will call the method `main` of `5_setup.py` (`5_setup.py` is the same as `4_rc_file.py` but everything is wrap in a method `main()`). The install the command line using pip:

```
pip install .
```

Then your new command line should work as expected:

```
foobar 2 3 --agg=max
```

An additionall tips is that if you use the flag `-e` when involing pip you will install the CLI in editable mode. In other words changes in the code will be reflected direcly when invoking you command, This is very handy when your CLI is still underdevelopemnt.

```
pip install -e .
```

## 5 Making the command line extandable

Once your command line is mature and many user are using it and adding feature, you may want to have a plugin system. So that your cli only contains the core features but other user can extand it. 

I learn the trick from [that article](https://amir.rachum.com/blog/2017/07/28/python-entry-points/). Often when developing an open source tool you whish to leave some room for other ro extend the fonctionlities of your CLI. On the other hand not every feature is usefull for the communauty. Therfore you may want to keep that specific feature out of the core and instead have a pluggin mechanism to make it optional. 

In summary this methods is an easy way to create a pluggin system for your CLI.

In our current implementation we can define which aggregation function we want to use with the flag `--agg`. We havent implemented any concrete action base on that flag yet. It was not usefult to demonstrate the previous examples. Lets fix that.

Implement a methods that takes a list of number, the name of an aggregator and a map of aggretor.

```python
def aggregate(N: list, agg_name, aggregators):
  if agg_name in aggregators:
    agg = aggregators[agg_name]
    return agg([int(i) for i in N])
  else:
    print(f"Aggregation function {agg_name} is not implemented")
    return 0
```

The function can be used as followed:

```python
aggregators = {
        'sum': sum,
        'max': max,
    }
result = aggregate(arguments["N"], arguments["--agg"], aggregators)
```

With this approach you are limited by the aggregators you listed in your dictionnary. What if someone wants to provide an pluggin for your system with very fancy operators to apply to a sequence of number? 

Well it is not too difficult with python `entry_points`. Lets refactor our code to make it extandable.

```python
aggregators = get_aggregators()
result = aggregate(arguments["N"], arguments["--agg"], aggregators)
```

The `get_aggregators` function will read all `entry_points` named `aggregators` and add them to our dictionnary of possible action.

```python
import pkg_resources

def get_aggregators():
    agg = {
        'sum': sum,
        'max': max,
    }
    for entry_point in pkg_resources.iter_entry_points('aggregators'):
        agg[entry_point.name] = entry_point.load()
    return agg
```

Now simply create a new package that define an `entry_points` named `aggregators` and install it.

Here is a `setup.py` to install your new pluggin. Notice the line `fancy = fancy:main` it mean that the aggregator call fancy referes to the file `fancy.py` and method `main` in yo plugin package.

```python
from setuptools import setup

setup(
    name='fancy_agg',
    entry_points={
        'aggregators': [
            'fancy = fancy:main',
        ],
    }
)
```

Here is a very fancy now operator

```python
def main(N: list):
    print("fancy Aggregator")
    return 42
```

Now install you new package, mine is called `extandable_fancy_aggregator`

```
python -m pip install -e ./extandable_fancy_aggregator
```

Try it for yourself

```
python .\6_extandable.py 1 2 --agg=fancys
```

## Conclusion

As you Python script grow into a full fledge command line there is at least five element presented above that I try to add. I like to diecribe them as Quality of life improvement.

1. Make my life easy when it comes to parsing aguments
2. Implement a dry-run to keep things under controle
3. Implement `.rc` because the command as grown bigger and I hate to write long command lines.
4. Install the script as a full fledge command line that I can use from anymere
5. Make the Command line extandable to faster collabortion and keep the core as small as possible