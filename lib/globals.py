"""
Global configuration of the project.
All hardcoded paths should be (theoretically) here.
"""
from __future__ import print_function

import logging
import os
from pygments.styles import get_all_styles

MYDIR = os.path.abspath(os.path.join(__file__, '..', '..'))
REDISHOST = 'redis'

ANSI2HTML = os.path.join(MYDIR, "share/ansi2html.sh")

LOG_FILE = os.path.join(MYDIR, 'log/main.log')
FILE_QUERIES_LOG = os.path.join(MYDIR, 'log/queries.log')
TEMPLATES = os.path.join(MYDIR, 'share/templates')
STATIC = os.path.join(MYDIR, 'share/static')
PATH_VIM_ENVIRONMENT = os.path.join(MYDIR, 'share/vim')

USE_OS_PACKAGES = False # change it False if you pull cheat sheets repositories from GitHub
if USE_OS_PACKAGES:
    PATH_TLDR_PAGES = "/home/igor/.tldr/cache/pages/*/*.md"
    PATH_CHEAT_PAGES = "/usr/local/lib/python2.7/dist-packages/cheat/cheatsheets/*"
    PATH_CHEAT_SHEETS = "/home/igor/cheat.sheets/sheets/"
    PATH_CHEAT_SHEETS_SPOOL = "/home/igor/cheat.sheets/spool/"
    PATH_LEARNXINY = "/home/igor/git/github.com/adambard/learnxinyminutes-docs"
else:
    PATH_TLDR_PAGES = os.path.join(MYDIR, "cheatsheets/tldr/*/*.md")
    PATH_CHEAT_PAGES = os.path.join(MYDIR, "cheatsheets/cheat/*")
    PATH_CHEAT_SHEETS = os.path.join(MYDIR, "cheatsheets/sheets/")
    PATH_CHEAT_SHEETS_SPOOL = os.path.join(MYDIR, "cheatsheets/spool/")
    PATH_LEARNXINY = os.path.join(MYDIR, "cheatsheets/learnxinyminutes-docs")

COLOR_STYLES = sorted(list(get_all_styles()))

MALFORMED_RESPONSE_HTML_PAGE = open(os.path.join(STATIC, 'malformed-response.html')).read()

def error(text):
    """
    Log error `text` and produce a RuntimeError exception
    """
    if not text.startswith('Too many queries'):
        print(text)
    logging.error("ERROR %s", text)
    raise RuntimeError(text)

def log(text):
    """
    Log error `text` (if it does not start with 'Too many queries')
    """
    if not text.startswith('Too many queries'):
        print(text)
        logging.info(text)
