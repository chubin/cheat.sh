"""
"""

# pylint: disable=relative-import,wrong-import-position,unused-argument,abstract-method

from gevent.monkey import patch_all
from gevent.subprocess import Popen, PIPE

from .adapter import Adapter

class CommandAdapter(Adapter):
    """
    """

    _command = []

    def _get_command(self, topic, request_options=None):
        return self._command

    def _get_page(self, topic, request_options=None):
        cmd = self._get_command(topic, request_options=request_options)
        if cmd:
            proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
            answer = proc.communicate()[0].decode('utf-8')
            return answer
        return ""

class Fosdem(CommandAdapter):

    """
    Show the output of the `current-fosdem-slide` command,
    which shows the current slide open in some terminal.
    This was used during the talk at FOSDEM 2019.

    https://www.youtube.com/watch?v=PmiK0JCdh5A

    `sudo` is used here beause the session was running under
    a different user; to be able to use the command via sudo,
    the following `/etc/suders` entry was added:

    srv    ALL=(ALL:ALL) NOPASSWD: /usr/local/bin/current-fosdem-slide

    Here `srv` is the user under which the cheat.sh server was running
    """

    _adapter_name = "fosdem"
    _output_format = "ansi"
    _pages_list = [":fosdem"]
    _command = ["sudo", "/usr/local/bin/current-fosdem-slide"]

class Translation(CommandAdapter):
    """
    """

    _adapter_name = "translation"
    _output_format = "text"
    _cache_needed = True

    def _get_page(self, topic, request_options=None):
        from_, topic = topic.split('/', 1)
        to_ = request_options.get('lang', 'en')
        if '-' in from_:
            from_, to_ = from_.split('-', 1)

        return ["/home/igor/cheat.sh/bin/get_translation",
                from_, to_, topic.replace('+', ' ')]
