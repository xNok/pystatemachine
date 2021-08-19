# 5 Tips to Create Better Command Line 

Welcome to the instructions for [5 Tips to Customise Python Command-Line Interfaces](https://betterprogramming.pub/5-tips-to-customise-python-command-line-interfaces-691b0b39f610?sk=5ac5a76c740bd04f5881af8a485a68a0).

This repo is originally dedicated to Python State Machine. But as usual, when I start working side-projects, I get a lot of article ideas.

## Setup


1. Create a Python virtual environment to try the demos

```
python -m venv venv
```

2. Acticate your virtual environnements

```
source ./venv/Scripts/activate
```

3. Install dependencies 

```
python -m pip install -r requirements.txt
```

## 1 Choose the right tool to parse your arguments

`.\1_argparse.py` demonstrate how to parse arguments with `argparse`

```
python .\1_argparse.py 1 2
```

`2_docopt` demonstrate how to parse arguments with `docopt`

```
python .\2_docopt.py 1 2
```

## 2 Implement a dry run

`3_dryable.py` demonstrate how to implement a dry run with `dryable`

```
.\3_dryable.py 1 2 --dry-run
```

## 3 Creating a .rc file

`4_rc_file.py` demonstrate how to implement a `.rc` file with `docopt`

```
python .\4_rc_file.py 1 2
```

## 4 Installing the Command Line

`setup.py` and `5_setup.py` demonstrate how to install a command line

```
python -m pip install -e .
```

Now you can call the command `foobar`

```
foobar 2 3 --agg=max
```

## 5 Making the command line extendable


```
cd extandable_fancy_aggregator
python -m pip install -e .
```

```
python .\6_extandable.py 1 2 --agg=fancy
```

## Other articles

* [No Code Argument Parsing for Command-Line Interfaces with docopt](https://medium.com/codex/no-code-argument-parsing-for-command-line-interfaces-79b17a3813f2?sk=680439c5fc3269c513d6010dd4d5ba8e)