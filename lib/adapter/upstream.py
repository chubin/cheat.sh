"""
Adapter for an external cheat sheets service (i.e. for cheat.sh)

Configuration parameters:

    upstream.url
    upstream.timeout
"""

# pylint: disable=relative-import

import textwrap
import requests

from config import CONFIG
from .adapter import Adapter

def _are_you_offline():
    return textwrap.dedent(
        """
         .
                         Are you offline?
            _________________
           | | ___________ |o|   Though it could be theoretically possible
           | | ___________ | |   to use cheat.sh fully offline,
           | | ___________ | |   and for *the programming languages questions* too,
           | | ___________ | |   this very feature is not yet implemented.
           | |_____________| |
           |     _______     |   If you find it useful, please visit
           |    |       |   ||   https://github.com/chubin/issues/140
           | DD |       |   V|   and drop a couple of lines to encourage
           |____|_______|____|   the authors to develop it as soon as possible

         .
            """)

class UpstreamAdapter(Adapter):

    """
    Connect to the upstream server `CONFIG["upstream.url"]` and fetch
    response from it. The response is supposed to have the "ansi" format.
    If the server does not respond within `CONFIG["upstream.timeout"]` seconds,
    or if a connection error occurs, the "are you offline" banner is displayed.

    Answers are by default cached; the failure answer is marked with the no-cache
    property ("cache": False).
    """

    _adapter_name = "upstream"
    _output_format = "ansi"
    _cache_needed = False

    def _get_page(self, topic, request_options=None):

        options_string = "&".join(["%s=%s" % (x, y) for (x, y) in request_options.items()])
        url = CONFIG["upstream.url"].rstrip('/') \
                + '/' + topic.lstrip('/') \
                + "?" + options_string
        try:
            response = requests.get(url, timeout=CONFIG["upstream.timeout"])
            answer = {"cache": False, "answer": response.text}
        except requests.exceptions.ConnectionError:
            answer = {"cache": False, "answer":_are_you_offline()}
        return answer

    def _get_list(self, prefix=None):
        return []
