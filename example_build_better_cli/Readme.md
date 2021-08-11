# 5 Tips to to Create Better Command Line Interface

1. Create a Python virtual environnement to try this demos

```
python -m venv venv
```

2. Acticate your virtual environnements

```
source ./venv/Scripts/activate
```

3. Install dependancies 

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

`setup.py` and `5_setup.py`demonstrate how to install a command line

```
python -m pip install -e .
```

Now you can call the command `foobar`

```
foobar 2 3 --agg=max
```

## 5 Making the command line extandable


```
cd extandable_fancy_aggregator
python -m pip install -e .
```

```
python .\6_extandable.py 1 2 --agg=fancy
```

