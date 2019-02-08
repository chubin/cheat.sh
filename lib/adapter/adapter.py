import abc

class Adapter(object):
    def __init__(self):
        self._list = self._get_list()

    @abc.abstractmethod
    def _get_list(self):
        return []

    def get_list(self):
        return self._list

    def is_found(self, topic):
        return topic in self._list

    @abc.abstractmethod
    def get_page(self, topic, request_options=None):
        pass
