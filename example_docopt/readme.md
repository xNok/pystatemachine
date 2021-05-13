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

```java
Map<String, Object> arguments =
        new Docopt(doc).parse(args);
```

Of course there is some differences specific to each language, you will find all the details in the documentation. The core of using docopt is to understand the [POSIX utility conventions](https://pubs.opengroup.org/onlinepubs/009695399/basedefs/xbd_chap12.html). This is way the first part of this Story will be language agnostique, but I reserved some tricks at the end for Pythonist to writter better cli.