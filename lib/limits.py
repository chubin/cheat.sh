"""
Connection limitation.

Number of connections from one IP is limited.
We have nothing against scripting and automated queries.
Even the opposite, we encourage them. But there are some
connection limits that even we can't handle.
Currently the limits are quite restrictive, but they will be relaxed
in the future.

Usage:

        limits = Limits()
        not_allowed = limits.check_ip(ip_address)
        if not_allowed:
            return "ERROR: %s" % not_allowed
"""

import time
from globals import log

_WHITELIST = ['5.9.243.177']

def _time_caps(minutes, hours, days):
    return {
        'min':   minutes,
        'hour':  hours,
        'day':   days,
        }

class Limits(object):
    """
    Queries limitation (by IP).

    Exports:

        check_ip(ip_address)
    """

    def __init__(self):
        self.intervals = ['min', 'hour', 'day']

        self.divisor = _time_caps(60, 3600, 86400)
        self.limit = _time_caps(30, 600, 1000)
        self.last_update = _time_caps(0, 0, 0)

        self.counter = {
            'min':      {},
            'hour':     {},
            'day':      {},
            }

        self._clear_counters_if_needed()

    def _log_visit(self, interval, ip_address):
        if ip_address not in self.counter[interval]:
            self.counter[interval][ip_address] = 0
        self.counter[interval][ip_address] += 1

    def _limit_exceeded(self, interval, ip_address):
        visits = self.counter[interval][ip_address]
        limit = self._get_limit(interval)
        return  visits > limit

    def _get_limit(self, interval):
        return self.limit[interval]

    def _report_excessive_visits(self, interval, ip_address):
        log("%s LIMITED [%s for %s]" % (ip_address, self._get_limit(interval), interval))

    def check_ip(self, ip_address):
        """
        Check if `ip_address` is allowed, and if not raise an RuntimeError exception.
        Return True otherwise
        """
        if ip_address in _WHITELIST:
            return None
        self._clear_counters_if_needed()
        for interval in self.intervals:
            self._log_visit(interval, ip_address)
            if self._limit_exceeded(interval, ip_address):
                self._report_excessive_visits(interval, ip_address)
                return ("Not so fast! Number of queries per %s is limited to %s"
                        % (interval, self._get_limit(interval)))
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
            if current_time // self.divisor[interval] != self.last_update[interval]:
                self.counter[interval] = {}
                self.last_update[interval] = current_time / self.divisor[interval]
