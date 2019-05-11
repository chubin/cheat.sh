"""
Adapter for the curlable latencies numbers (chubin/late.nz)
This module can be an example of a adapter for a python project.

The adapter exposes one page ("latencies") and several its aliases
("latencies", "late.nz", "latency")
"""

# pylint: disable=relative-import

import sys
import os
from .git_adapter import GitRepositoryAdapter

class Latenz(GitRepositoryAdapter):

    """
    chubin/late.nz Adapter
    """

    _adapter_name = "late.nz"
    _output_format = "ansi"
    _repository_url = "https://github.com/chubin/late.nz"

    def _get_page(self, topic, request_options=None):
        sys.path.append(os.path.join(self.local_repository_location(), 'bin'))
        import latencies
        return latencies.render()

    def _get_list(self, prefix=None):
        return ['latencies']

    def is_found(self, topic):
        return topic.lower() in ['latencies', 'late.nz', 'latency']
