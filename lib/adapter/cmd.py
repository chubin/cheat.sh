"""
"""

# pylint: disable=unused-argument,abstract-method

import os.path
import re
from subprocess import Popen, PIPE

from .adapter import Adapter


def _get_abspath(path):
    """Find absolute path of the specified `path`
    according to its
    """

    if path.startswith("/"):
        return path

    import __main__
    return os.path.join(
        os.path.dirname(os.path.dirname(__main__.__file__)),
        path)

class CommandAdapter(Adapter):
    """
    """

    _command = []

    def _get_command(self, topic, request_options=None):
        return self._command

    def _get_page(self, topic, request_options=None):
        cmd = self._get_command(topic, request_options=request_options)
        if cmd:
            try:
                proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
                answer = proc.communicate()[0].decode('utf-8', 'ignore')
            except OSError:
                return "ERROR of the \"%s\" adapter: please create an issue" % self._adapter_name
            return answer
        return ""

class Fosdem(CommandAdapter):

    """
    Show the output of the `current-fosdem-slide` command,
    which shows the current slide open in some terminal.
    This was used during the talk at FOSDEM 2019.

    https://www.youtube.com/watch?v=PmiK0JCdh5A

    `sudo` is used here because the session was running under
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


class AdapterRfc(CommandAdapter):
    """
    Show RFC by its number.
    Exported as: "/rfc/NUMBER"
    """

    _adapter_name = "rfc"
    _output_format = "text"
    _cache_needed = True
    _command = ["share/adapters/rfc.sh"]

    def _get_command(self, topic, request_options=None):
        cmd = self._command[:]
        if not cmd[0].startswith("/"):
            cmd[0] = _get_abspath(cmd[0])

        # cut rfc/ off
        if topic.startswith("rfc/"):
            topic = topic[4:]

        return cmd + [topic]

    def _get_list(self, prefix=None):
        return list("rfc/%s" % x for x in range(1, 8649))

    def is_found(self, topic):
        return True

class AdapterOeis(CommandAdapter):
    """
    Show OEIS by its number.
    Exported as: "/oeis/NUMBER"
    """

    _adapter_name = "oeis"
    _output_format = "text+code"
    _cache_needed = True
    _command = ["share/adapters/oeis.sh"]

    @staticmethod
    def _get_filetype(topic):
        if "/" in topic:
            language = topic.split("/")[-1].lower()
            return language
        return "bash"

    def _get_command(self, topic, request_options=None):
        cmd = self._command[:]
        if not cmd[0].startswith("/"):
            cmd[0] = _get_abspath(cmd[0])

        # cut oeis/ off
        # Replace all non (alphanumeric, '-', ':') chars with Spaces to delimit args to oeis.sh
        if topic.startswith("oeis/"):
            topic = topic[5:]

            suffix = ""
            if topic.endswith("/:list"):
                suffix = " :list"
                topic = topic[:-6]

            topic = re.sub('[^a-zA-Z0-9-:]+', ' ', topic) + suffix

        return cmd + [topic]

    def is_found(self, topic):
        return True

class AdapterChmod(CommandAdapter):
    """
    Show chmod numeric values and strings
    Exported as: "/chmod/NUMBER"
    """

    _adapter_name = "chmod"
    _output_format = "text"
    _cache_needed = True
    _command = ["share/adapters/chmod.sh"]

    def _get_command(self, topic, request_options=None):
        cmd = self._command[:]

        # cut chmod/ off
        # remove all non (alphanumeric, '-') chars
        if topic.startswith("chmod/"):
            topic = topic[6:]
            topic = re.sub('[^a-zA-Z0-9-]', '', topic)


        return cmd + [topic]

    def is_found(self, topic):
        return True
