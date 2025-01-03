"""
Import all adapters from the current directory
and make them available for import as
    adapter_module.AdapterName
"""

# pylint: disable=wildcard-import,relative-import

import glob
from os.path import basename, dirname, isfile, join

__all__ = [
    basename(f)[:-3]
    for f in glob.glob(join(dirname(__file__), "*.py"))
    if isfile(f) and not f.endswith('__init__.py')]

from . import *
from .adapter import all_adapters
