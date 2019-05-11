"""
Standalone wrapper for the cheat.sh server.
"""

from __future__ import print_function

import sys
import textwrap
try:
    import urlparse
except ModuleNotFoundError:
    import urllib.parse as urlparse

import config
config.CONFIG["cache.type"] = "none"

import cheat_wrapper
import options

def show_usage():
    """
    Show how to use the program in the standalone mode
    """

    print(textwrap.dedent("""
        Usage:

            lib/standalone.py [OPTIONS] QUERY

        For OPTIONS see :help
    """)[1:-1])

def parse_cmdline(args):
    """
    Parses command line arguments and returns
    query and request_options
    """

    if not args:
        show_usage()
        sys.exit(0)

    query_string = " ".join(args)
    parsed = urlparse.urlparse("https://srv:0/%s" % query_string)
    request_options = options.parse_args(
        urlparse.parse_qs(parsed.query, keep_blank_values=True))

    query = parsed.path.lstrip("/")
    if not query:
        query = ":firstpage"

    return query, request_options


def main(args):
    """
    standalone wrapper for cheat_wrapper()
    """

    query, request_options = parse_cmdline(args)
    answer, _ = cheat_wrapper.cheat_wrapper(query, request_options=request_options)
    sys.stdout.write(answer)

if __name__ == '__main__':
    main(sys.argv[1:])
