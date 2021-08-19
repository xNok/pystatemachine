# No Code Argument Parsing for Command-Line Interfaces

When writing a command-line interface (CLI), you can save a lot of time and effort by using one of the dedicated libraries to parse arguments. Parsing all the arguments, writing the help message, and keeping the documentation in sync can be pretty time-consuming. What if you could only write the help message and use a single line of code to create your CLI? This is the deal that [docopt](https://github.com/docopt) offers you.

> You know what's awesome? It's when the option parser is generated based on the beautiful help message that you write yourself! This way, you don't need to write this stupid repeatable parser-code, and instead can write only the help message--the way you want it. (docotp author)

This library, in my opinion, stands out from its competitors:
* docopt is available for many different languages: Python, Go, Rust, JAVA, Ruby, C, C++, PHP, and a few others.
* Very little code to write.
* You have to maintain the documentation. Those new arguments you want to have won't be considered if you don't update the help message.
* This library doesn't impose a convention on how to design the command line. It simply parses the arguments and provides you a Map of all values.

In this article, I will only be going over basic using Python. However, you will mainly write the documentation. So I considere the tutorial as language agnostic.

> Plus you can try it out [in you browser](http://try.docopt.org/)

For languages other that, you will change a single line of code: 

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

There is some differences specific to each language, you will find all the details in the documentation. 

The core of using `docopt` is to understand the [POSIX Utility Conventions](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html) and [GNU Standards for Command Line Interfaces](https://www.gnu.org/prep/standards/html_node/Command_002dLine-Interfaces.html). The second (GNU) one being an extention of the first one (POSIX).

By using CLI like `git` you are probably already familiar with the syntax anyway.

## Designing a Command Line Interface with docopt

### The bare minimum to create a CLI

As you can see below, you can start with:
* A name
* The two foundamental usage. Displaying the help message and the version.
* A description of Options availables

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
```

### The basing building block of a command line

I counted five foundamental building black for command lines: *Positional Arguments*, *flags*, *long-named options*, *flags with argument*, *long-named options*.

* *Positional Arguments*: These are the most basic element of command lines, they are identified by there position in the comment line, such as `cli arg1 arg2`. In an help message the are often between angle brackets: `cli <arg1> <arg2>` or in upper case `cli ARG1 ARG2`
* *flags*: these are single alphanumeric character prefixed with `-` such as `-a`, `-b`. Flags can be grouped all together `-ab` = `-a -b`
* *long-named options*: These are words prefixed with `--` such as `--verbose`. There main pupose is to build more human readable command line. It is very commun to have both flags and long-named for each possible arguments.
* *flags with argument*: These are flag that simpla expect a parameter alongside them `-p path`. Again arguments are ofter place between angle brackets `-p <path>`
* *long-named options*: These are similare to flags with argument, but several conventions are accepted `--long-d <argument>` `--long-d=<argument>`

This is how you would create a simple command line with these fives elements:

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

This command-line definition will produce a Map of all the parameters provided. It is important to know that:
* Every flag, long-name and arguments are in the result Map with a default value (it would be `False` if the flag is not used or `None` if an argument was expected).
* The default value can be overriten by adding `[default: 10]` to the Option documentation

Here is an example of Map produce by the previous definition:

```
{'--help': False,
 '--long-b': False,
 '--long-d': 'rwerwer',
 '--version': False,
 '-a': False,
 '-c': 'test',
 '<path>': '.'}
```

## Arguments validation and Complex command lines

To perfectly define what is allowed in you command-line you will need the four following operators:

* brackets `[ ]` defines optional argument
* parens "( )" defines optional argument
* pipes "|" are used inside `[ ]` or "( )" to define mutually exclusive arguments. `[-a |-b]` flag `-a` or `-b` is optional but both cannot be used at the same time.
* ellipsis "..." are used to define argument that can be repeated. [-v...] means the flag `-v` can be used any number of times (ex: `-vvvv`)

This mechanism adds a layer of validation to you command-line. If a command is invalide with regards to the usage patter you defined then `docopt` will display the help message.
