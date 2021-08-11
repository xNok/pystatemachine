# You write the help message docopt write the code

When writing a command-line interface (cli) you can save a lot of time and effort by using one of the dedicated libraries out there. Indeed parsing all the arguments, writing the help message, and keeping the documentation in sync can be pretty time-consuming. What if you could only write the help message and use a single line of code to create your cli? This is the deal that [docopt](https://github.com/docopt) offers you.

> You know what's awesome? It's when the option parser is generated based on the beautiful help message that you write yourself! This way you don't need to write this stupid repeatable parser-code, and instead can write only the help message--the way you want it. (docotp author)

This library, in my opinion, stands out from its competitors:
* docopt is available for many different languages: Python, Go, Rust, JAVA, Ruby, C, C++, PHP, and a few others.
* Very little code to write. This library doesn't come with a convention on how to design the command line. It simply parses the arguments and provides you a Map of all the values.
* You have to maintain the documentation. Those new arguments you want to have won't be considered if you don't update the help message.

In this article, I will only be going over basic using Python. However we are mainly going to write documentation. For other languages you will change a single line of code: 

In Python:

```python
arguments = docopt(__doc__)
```

In Go:

```go
arguments, _ := docopt.ParseDoc(usage)
```

In JAVA
s
```java
Map<String, Object> arguments =
        new Docopt(doc).parse(args);
```

Of course there is some differences specific to each language, you will find all the details in the documentation. The core of using docopt is to understand the s. By using other cli like `git` you probably are already familiar with the syntax. This is I consider this tutorial to be language agnostique.

## Designing a Command Line Interface with docopt

### The bare minumu to create a cli

```python
"""
CLI Utils

Usage:
  utility_name (-h | --help)
  utility_name --version

Options:
    -h --help             Show the help message.
    --version             Show version.
"""

### The basing building block of a command line

* *Positional Arguments*: These are le most basic element of command lines, they are identified by there position in the comment line, such as `cli arg1 arg2`. In an help message the are often between angle brackets: `cli <arg1> <arg2>` or in upper case `cli ARG1 ARG2`
* *flags*: these are single alphanumeric character prefixed with `-` such as `-a`, `-b`. Flags can be grouped all together `-ab` = `-a -b`
* *long-named options*: These are words prefixed with `--` such as `--verbose`. There main pupose is to build more human readable command line. It is very commun to have both flags and long-named for each possible arguments.
* *flags with argument*: These are flag that simpla expect a parameter alongside them `-p path`. Again arguments are ofter place between angle brackets `-p <path>`
* *long-named options*: These are similare to flags with argument, but several conventions are accepted `--long-d <argument>` `--long-d=<argument>`

This is how you would create a simple command line with these 5 elements:

```python
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
    -h --help             Show the help message.
    --version             Show version.
"""

from docopt import docopt


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Utility 20.0')
    print(arguments)
```

This command line definition will produce a Map of all the parameter provided. It is important to know that:
* Every flag, long-name and arguments are in the result Map with a default value (it would be `False` if the flag is not used or `None` if an argument was expected).
* The default value can be overriten by adding `[default: 10]` to the Option documentation


```
{'--help': False,
 '--long-b': False,
 '--long-d': 'rwerwer',
 '--version': False,
 '-a': False,
 '-c': 'test',
 '<path>': '.'}
```

### Validation argument of a command line

The command line convention let you know exactly the behavior of arguments and it easy easy to know which arguments ar required, which one are optional, which argument car work together, which argument are not compatible, wich argument ca be repeated, etc.
