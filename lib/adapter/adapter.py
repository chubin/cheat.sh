import abc

class Adapter(object):

    _adapter_name = None
    _output_format = 'code'

    def __init__(self):
        self._list = {None: self._get_list()}

    @abc.abstractmethod
    def _get_list(self, prefix=None):
        return []

    def get_list(self, prefix=None):
        """
        Return available pages for `prefix`
        """

        if prefix in self._list:
            return self._list[prefix]

        self._list[prefix] = self._get_list(prefix=prefix)
        return self._list[prefix]

    def is_found(self, topic):
        """
        check if `topic` is available
        CAUTION: only root is checked
        """
        return topic in self._list[None]

    @abc.abstractmethod
    def _get_page(self, topic, request_options=None):
        """
        Return page for `topic`
        """
        pass

    def _get_output_format(self, _topic):
        return self._output_format

    def get_page_dict(self, topic, request_options=None):
        """
        Return page dict for `topic`
        """
        answer_dict = {
            'topic': topic,
            'topic_type': self._adapter_name,
            'answer': self._get_page(topic, request_options=request_options),
            'format': self._get_output_format(topic),
            }
        return answer_dict
