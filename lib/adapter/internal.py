"""
Configuration parameters:

    frontend.styles
    path.internal.pages
"""

import sys
import os
import collections

try:
    from rapidfuzz import process, fuzz
    _USING_FUZZYWUZZY=False
except ImportError:
    from fuzzywuzzy import process, fuzz
    _USING_FUZZYWUZZY=True

from config import CONFIG
from .adapter import Adapter
from fmt.internal import colorize_internal

_INTERNAL_TOPICS = [
    ":cht.sh",
    ":bash_completion",
    ":emacs",
    ":emacs-ivy",
    ":firstpage",
    ":firstpage-v1",
    ":firstpage-v2",
    ":fish",
    ":help",
    ":intro",
    ":list",
    ":post",
    ":styles",
    ":styles-demo",
    ":vim",
    ":zsh",
    ]

_COLORIZED_INTERNAL_TOPICS = [
    ':intro',
]

class InternalPages(Adapter):

    _adapter_name = 'internal'
    _output_format = 'ansi'

    def __init__(self, get_topic_type=None, get_topics_list=None):
        Adapter.__init__(self)
        self.get_topic_type = get_topic_type
        self.get_topics_list = get_topics_list

    def _get_stat(self):
        stat = collections.Counter([
            self.get_topic_type(topic)
            for topic in self.get_topics_list()
        ])

        answer = ""
        for key, val in stat.items():
            answer += "%s %s\n" % (key, val)
        return answer

    @staticmethod
    def get_list(prefix=None):
        return _INTERNAL_TOPICS

    def _get_list_answer(self, topic, request_options=None):
        if '/' in topic:
            topic_type, topic_name = topic.split('/', 1)
            if topic_name == ":list":
                topic_list = [x[len(topic_type)+1:]
                              for x in self.get_topics_list()
                              if x.startswith(topic_type + "/")]
                return "\n".join(topic_list)+"\n"

        answer = ""
        if topic == ":list":
            answer = "\n".join(x for x in self.get_topics_list()) + "\n"

        return answer

    def _get_page(self, topic, request_options=None):
        if topic.endswith('/:list') or topic.lstrip('/') == ':list':
            return self._get_list_answer(topic)

        answer = ""
        if topic == ':styles':
            answer = "\n".join(CONFIG["frontend.styles"]) + "\n"
        elif topic == ":stat":
            answer = self._get_stat()+"\n"
        elif topic in _INTERNAL_TOPICS:
            answer = open(os.path.join(CONFIG["path.internal.pages"], topic[1:]+".txt"), "r").read()
            if topic in _COLORIZED_INTERNAL_TOPICS:
                answer = colorize_internal(answer)

        return answer

    def is_found(self, topic):
        return (
            topic in self.get_list()
            or topic.endswith('/:list')
        )

class UnknownPages(InternalPages):

    _adapter_name = 'unknown'
    _output_format = 'text'

    @staticmethod
    def get_list(prefix=None):
        return []

    @staticmethod
    def is_found(topic):
        return True

    def _get_page(self, topic, request_options=None):
        topics_list = self.get_topics_list()
        if topic.startswith(':'):
            topics_list = [x for x in topics_list if x.startswith(':')]
        else:
            topics_list = [x for x in topics_list if not x.startswith(':')]

        if _USING_FUZZYWUZZY:
            possible_topics = process.extract(topic, topics_list, scorer=fuzz.ratio)[:3]
        else:
            possible_topics = process.extract(topic, topics_list, limit=3, scorer=fuzz.ratio)
        possible_topics_text = "\n".join([("    * %s %s" % (x[0], int(x[1]))) for x in possible_topics])
        return """
Unknown topic.
Do you mean one of these topics maybe?

%s
    """ % possible_topics_text

class Search(Adapter):

    _adapter_name = 'search'
    _output_format = 'text'
    _cache_needed = False

    @staticmethod
    def get_list(prefix=None):
        return []

    def is_found(self, topic):
        return False
