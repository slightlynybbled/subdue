# Purpose

This project is intended to bring together lots of different hardware
projects into a single unified API to ease hardware test development.
Using this project, it should be easier to write a Python-driven hardware
test using the old Python favorites.  In many ways, this is somewhat
equivalent to LabView in functionality, but with all of the advantages
of Python.  Enjoy!

# Installation Requirements

You will need to have a working installation of 
[Python 3.5](https://www.python.org/downloads/) environment to run
the AMS Hardware Suite.  Installation of some or all software may require
administrative access.

It is recommended that `python` be added to the `PATH` and that `*.py`
extensions are associated with `python`.

# Installation Instructions

To install, simply `pip install subdue`.  Note that there are several
external dependencies.  See the documentation for details.

## Examples

Several examples are provided for your convenience within the 
`/examples` directory.  Simply run the example in your python environment.
Note that the examples will require attached hardware, hardware drivers,
and may require other packages (such as `requests`).

# Contributions

Please use the [issues](https://github.com/slightlynybbled/subdue/issues)
to request support for new hardware.  As I likely do not have a set of 
hardware for development, I may not be able to add functionality to the
library with confidence.  Pull requests are welcome!
