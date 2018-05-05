"""
Connection limitatation.

Number of connections from one IP is limited.
We have nothing against scripting and automated queries,
even in opposite, we encourage them, but there are some
connection limits that even we can't handle.
Currently the limits set low, but they will be relaxed
in future.

Usage:

        limits = Limits()
        not_allowed = limits.check_ip(ip_address)
        if not_allowed:
            return "ERROR: %s" % not_allowed
"""

import time
from globals import log

_WHITELIST = ['5.9.243.177']

class Limits(object):
    """
    Queries limitation (by IP).

    Exports:

        check_ip(ip_address)
    """

    def __init__(self):
        self.intervals = ['min', 'hour', 'day']
        self.divisor = {
            'min':      60,
            'hour':     3600,
            'day':      86400,
            }
        self.counter = {
            'min':      {},
            'hour':     {},
            'day':      {},
            }
        self.limit = {
            'min':      30,
            'hour':     600,
            'day':      1000,
            }
        self.last_update = {
            'min':      0,
            'hour':     0,
            'day':      0,
            }
        self._clear_counters_if_needed()

    def check_ip(self, ip_address):
        """
        Check if `ip_address` is allowed, and if not raise an RuntimeError exception.
        Return True otherwise
        """
        if ip_address in _WHITELIST:
            return None
        self._clear_counters_if_needed()
        for interval in self.intervals:
            if ip_address not in self.counter[interval]:
                self.counter[interval][ip_address] = 0
            self.counter[interval][ip_address] += 1
            if self.limit[interval] <= self.counter[interval][ip_address]:
                log("%s LIMITED [%s for %s]" % (ip_address, self.limit[interval], interval))
                return ("Not so fast! Number of queries per %s is limited to %s"
                        % (interval, self.limit[interval]))
        return None

    def reset(self):
        """
        Reset all counters for all IPs
        """
        for interval in self.intervals:
            self.counter[interval] = {}

    def _clear_counters_if_needed(self):
        current_time = int(time.time())
        for interval in self.intervals:
            if current_time / self.divisor[interval] != self.last_update[interval]:
                self.counter[interval] = {}
                self.last_update[interval] = current_time / self.divisor[interval]
