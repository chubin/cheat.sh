"""
Global functions that our used everywhere in the project.
Please, no global variables here.
For the configuration related things see `config.py`
"""

from __future__ import print_function

import sys
import logging

def fatal(text):
    """
    Fatal error function.

    The function is being used in the standalone mode only
    """
    sys.stderr.write("ERROR: %s\n" % text)
    sys.exit(1)

def error(text):
    """
    Log error `text` and produce a RuntimeError exception
    """
    if not text.startswith("Too many queries"):
        print(text)
    logging.error("ERROR %s", text)
    raise RuntimeError(text)

def log(text):
    """
    Log error `text` (if it does not start with 'Too many queries')
    """
    if not text.startswith("Too many queries"):
        print(text)
        logging.info(text)
