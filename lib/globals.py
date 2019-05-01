"""
Global configuration of the project.
All hardcoded pathes and other data should be
(theoretically) here.
"""
from __future__ import print_function

import sys
import logging
import os
import yaml
from pygments.styles import get_all_styles

DOCKERIZED = False      # set to True if the service is running in a Docker container

SERVER_ADDRESS = '0.0.0.0'
SERVER_PORT = 8002

MYDIR = os.path.abspath(os.path.join(__file__, '..', '..'))
_CONF_FILE = os.path.join(MYDIR, 'etc/config.yaml')

LOCAL_REPOSITORIES = os.path.join(os.environ['HOME'], '.cheat.sh', 'upstream')

if DOCKERIZED:
    REDISHOST = 'redis'
else:
    REDISHOST = 'localhost'

ANSI2HTML = os.path.join(MYDIR, "share/ansi2html.sh")

LOG_FILE = os.path.join(MYDIR, 'log/main.log')
FILE_QUERIES_LOG = os.path.join(MYDIR, 'log/queries.log')

TEMPLATES = os.path.join(MYDIR, 'share/templates')
STATIC = os.path.join(MYDIR, 'share/static')
PATH_VIM_ENVIRONMENT = os.path.join(MYDIR, 'share/vim')

USE_OS_PACKAGES = True  # set to False if you pull cheat sheets repositories from GitHub
if USE_OS_PACKAGES:
    PATH_CHEAT_SHEETS_SPOOL = "/home/igor/cheat.sheets/spool/"
    PATH_LEARNXINY = "/home/igor/git/github.com/adambard/learnxinyminutes-docs"
    ROSETTA_PATH = '/home/igor/git/github.com/acmeism/RosettaCodeData'
else:
    PATH_CHEAT_SHEETS_SPOOL = os.path.join(MYDIR, "cheatsheets/spool/")
    PATH_LEARNXINY = os.path.join(MYDIR, "cheatsheets/learnxinyminutes-docs")
    ROSETTA_PATH = os.path.join(MYDIR, "acmeism/RosettaCodeData")

GITHUB_REPOSITORY = {
    "late.nz"           :   'chubin/late.nz',
    "cheat.sheets"      :   'chubin/cheat.sheets',
    "cheat.sheets dir"  :   'chubin/cheat.sheets',
    "tldr"              :   'tldr-pages/tldr',
    "cheat"             :   'chrisallenlane/cheat',
    "learnxiny"         :   'adambard/learnxinyminutes-docs',
    "internal"          :   '',
    "search"            :   '',
    "unknown"           :   '',
}

CONFIG = {
    'adapters.active': [
        "tldr",
        "cheat",
        "fosdem",
        "translation",
        "rosetta",
        "late.nz",
        "question",
        "cheat.sheets",
        "cheat.sheets dir",
        "learnxiny",
        ],
    'adapters.mandatory': [
        "search",
        ],
    }

MAX_SEARCH_LEN = 20

#
# Reading configuration from etc/config.yaml
# config overrides default settings
#
if os.path.exists(_CONF_FILE):
    _CONFIG = yaml.load(_CONF_FILE, Loader=yaml.SafeLoader)
    if 'server' in _CONFIG:
        _SERVER_CONFIG = _CONFIG['server']
        if 'address' in _SERVER_CONFIG:
            SERVER_ADDRESS = _SERVER_CONFIG['address']
        if 'port' in _SERVER_CONFIG:
            SERVER_ADDRESS = _SERVER_CONFIG['port']


COLOR_STYLES = sorted(list(get_all_styles()))

MALFORMED_RESPONSE_HTML_PAGE = open(os.path.join(STATIC, 'malformed-response.html')).read()

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
