#pylint: disable=too-few-public-methods

"""
Developer keys validator
"""

import os

from config import CONFIG

class DevkeysChecker:

    """
    Developer keys validator class
    """

    def __init__(self):

        self._keys = {}
        self._load_keys()

    def check(self, key: str) -> str:
        """
        Check `key` and return True if it is valid.
        """
        return self._keys.get(key)

    def _load_keys(self) -> None:
        filename = self._get_keys_file()
        if not os.path.exists(filename):
            return
        with open(filename, "r") as f_keys:
            for line in f_keys.readlines():
                parts = line.strip().split()
                if len(parts) < 2:
                    continue
                self._keys[parts[0]] = parts[1]

    @staticmethod
    def _get_keys_file() -> str:
        return CONFIG["path.internal.keysfile"]

Devkeys = DevkeysChecker()
