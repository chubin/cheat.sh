"""
Global configuration of the project.

All configurable parameters are stored in the global variable CONFIG,
the only variable which is exported from the module.

Default values of all configuration parameters are specified
in the `_CONFIG` dictionary. Those parameters can be overridden
by three means:
    * config file `etc/config.yaml` located in the work dir
    * config file `etc/config.yaml` located in the project dir
      (if the work dir and the project dir are not the same)
    * environment variables prefixed with `CHEATSH_`

Configuration placement priorities, from high to low:
    * environment variables;
    * configuration file in the workdir
    * configuration file in the project dir
    * default values specified in the `_CONFIG` dictionary

If the work dir and the project dir are not the same, we do not
recommend that you use the config file located in the project dir,
except the cases when you use your own cheat.sh fork, and thus
configuration is a part of the project repository.
In all other cases `WORKDIR/etc/config.yaml` should be preferred.
Location of this config file can be overridden by the `CHEATSH_PATH_CONFIG`
environment variable.

Configuration parameters set by environment variables are mapped
in this way:
    * CHEATSH_ prefix is trimmed
    * _ replaced with .
    * the string is lowercased

For instance, an environment variable named `CHEATSH_SERVER_PORT`
specifies the value for the `server.port` configuration parameter.

Only parameters that imply scalar values (integer or string)
can be set using environment variables, for the rest config files
should be used. If a parameter implies an integer, and the value
specified by an environment variable is not an integer, it is ignored.
"""

from __future__ import print_function
import os

from pygments.styles import get_all_styles
#def get_all_styles():
#    return []

_ENV_VAR_PREFIX = "CHEATSH"

_MYDIR = os.path.abspath(os.path.join(__file__, '..', '..'))

def _config_locations():
    """
    Return three possible config locations
    where configuration can be found:
    * `_WORKDIR`, `_CONF_FILE_WORKDIR`, `_CONF_FILE_MYDIR`
    """

    var = _ENV_VAR_PREFIX + '_PATH_WORKDIR'
    workdir = os.environ[var] if var in os.environ \
        else os.path.join(os.environ['HOME'], '.cheat.sh')

    var = _ENV_VAR_PREFIX + '_CONFIG'
    conf_file_workdir = os.environ[var] if var in os.environ \
            else os.path.join(workdir, 'etc/config.yaml')

    conf_file_mydir = os.path.join(_MYDIR, 'etc/config.yaml')
    return workdir, conf_file_workdir, conf_file_mydir

_WORKDIR, _CONF_FILE_WORKDIR, _CONF_FILE_MYDIR = _config_locations()

_CONFIG = {
    "adapters.active": [
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
        "rfc",
        "oeis",
        "chmod",
        ],
    "adapters.mandatory": [
        "search",
        ],
    "cache.redis.db": 0,
    "cache.redis.host": "localhost",
    "cache.redis.port": 6379,
    "cache.redis.prefix": "",
    "cache.type": "redis",
    "frontend.styles": sorted(list(get_all_styles())),
    "log.level": 4,
    "path.internal.ansi2html": os.path.join(_MYDIR, "share/ansi2html.sh"),
    "path.internal.bin": os.path.join(_MYDIR, "bin"),
    "path.internal.bin.upstream": os.path.join(_MYDIR, "bin", "upstream"),
    "path.internal.malformed": os.path.join(_MYDIR, "share/static/malformed-response.html"),
    "path.internal.pages": os.path.join(_MYDIR, "share"),
    "path.internal.static": os.path.join(_MYDIR, "share/static"),
    "path.internal.templates": os.path.join(_MYDIR, "share/templates"),
    "path.internal.vim": os.path.join(_MYDIR, "share/vim"),
    "path.log.main": "log/main.log",
    "path.log.queries": "log/queries.log",
    "path.log.fetch": "log/fetch.log",
    "path.repositories": "upstream",
    "path.spool": "spool",
    "path.workdir": _WORKDIR,
    "routing.pre": [
        ("^$", "search"),
        ("^[^/]*/rosetta(/|$)", "rosetta"),
        ("^rfc/", "rfc"),
        ("^oeis/", "oeis"),
        ("^chmod/", "chmod"),
        ("^:", "internal"),
        ("/:list$", "internal"),
        ("/$", "cheat.sheets dir"),
        ],
    "routing.main": [
        ("", "cheat.sheets"),
        ("", "cheat"),
        ("", "tldr"),
        ("", "late.nz"),
        ("", "fosdem"),
        ("", "learnxiny"),
    ],
    "routing.post": [
        ("^[^/ +]*$", "unknown"),
        ("^[a-z][a-z]-[a-z][a-z]$", "translation"),
        ],
    "routing.default": "question",
    "upstream.url": "https://cheat.sh",
    "upstream.timeout": 5,
    "search.limit": 20,
    "server.bind": "0.0.0.0",
    "server.port": 8002,
    }

class Config(dict):
    """
    configuration dictionary that handles relative
    paths properly (making them relative to path.workdir)
    """

    def _absolute_path(self, val):
        if val.startswith('/'):
            return val
        return os.path.join(self['path.workdir'], val)

    def __init__(self, *args, **kwargs):
        dict.__init__(self)
        self.update(*args, **kwargs)

    def __setitem__(self, key, val):
        if key.startswith('path.') and not val.startswith('/'):
            val = self._absolute_path(val)
        dict.__setitem__(self, key, val)

    def update(self, *args, **kwargs):
        """
        the built-in __init__ doesn't call update,
        and the built-in update doesn't call __setitem__,
        so `update` should be overridden
        """

        newdict = dict(*args, **kwargs)
        if 'path.workdir' in newdict:
            self['path.workdir'] = newdict['path.workdir']

        for key, val in newdict.items():
            self[key] = val

def _load_config_from_environ(config):

    update = {}
    for key, val in config.items():
        if not isinstance(val, str) or isinstance(val, int):
            continue

        env_var = _ENV_VAR_PREFIX + '_' + key.replace('.', '_').upper()
        if not env_var in os.environ:
            continue

        env_val = os.environ[env_var]
        if isinstance(val, int):
            try:
                env_val = int(env_val)
            except (ValueError, TypeError):
                continue

        update[key] = env_val

    return update

def _get_nested(data, key):
    """
    Return value for a hierrachical key (like a.b.c).
    Return None if nothing found.
    If there is a key with . in the name, and a subdictionary,
    the former is preferred:

    >>> print(_get_nested({'a.b': 10, 'a':{'b': 20}}, 'a.b'))
    10
    >>> print(_get_nested({'a': {'b': 20}}, 'a.b'))
    20
    >>> print(_get_nested({'a': {'b': {'c': 30}}}, 'a.b.c'))
    30
    """

    if not data or not isinstance(data, dict):
        return None
    if '.' not in key:
        return data.get(key)
    if key in data:
        return data[key]

    parts = key.split('.')
    for i in range(len(parts))[::-1]:
        prefix = ".".join(parts[:i])
        if prefix in data:
            return _get_nested(data[prefix], ".".join(parts[i:]))

    return None

def _load_config_from_file(default_config, filename):
    import yaml

    update = {}
    if not os.path.exists(filename):
        return update

    with open(filename) as f:
        newconfig = yaml.load(f.read(), Loader=yaml.SafeLoader)
    for key, val in default_config.items():
        newval = _get_nested(newconfig, key)
        if newval is None:
            continue

        if isinstance(val, int):
            try:
                newval = int(newval)
            except (ValueError, TypeError):
                continue

        update[key] = newval

    return update

CONFIG = Config()
CONFIG.update(_CONFIG)
CONFIG.update(_load_config_from_file(_CONFIG, _CONF_FILE_MYDIR))
if _CONF_FILE_WORKDIR != _CONF_FILE_MYDIR:
    CONFIG.update(_load_config_from_file(_CONFIG, _CONF_FILE_WORKDIR))
CONFIG.update(_load_config_from_environ(_CONFIG))

if __name__ == "__main__":
    import doctest
    doctest.testmod()
