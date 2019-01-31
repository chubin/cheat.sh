import sys
import os
import glob
import collections

from fuzzywuzzy import process, fuzz

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from globals import MYDIR, COLOR_STYLES
from colorize_internal import colorize_internal

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
    ":share",
    ]

_COLORIZED_INTERNAL_TOPICS = [
    ':intro',
]

class InternalPages(object):

    def __init__(self, get_topic_type=None, get_topics_list=None):
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
    def get_list():
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

    def get_page(self, topic, request_options=None):
        if topic.endswith('/:list') or topic.lstrip('/') == ':list':
            return self._get_list_answer(topic)

        answer = ""
        if topic == ':styles':
            answer = "\n".join(COLOR_STYLES) + "\n"
        elif topic == ":stat":
            answer = self._get_stat()+"\n"
        elif topic in _INTERNAL_TOPICS:
            answer = open(os.path.join(MYDIR, "share", topic[1:]+".txt"), "r").read()
            if topic in _COLORIZED_INTERNAL_TOPICS:
                answer = colorize_internal(answer)

        return answer

    def is_found(self, topic):
        return topic in self.get_list()

class UnknownPages(InternalPages):

    @staticmethod
    def get_list():
        return []

    @staticmethod
    def is_found(topic):
        return False

    def get_page(self, topic, request_options=None):
        topics_list = self.get_topics_list()
        if topic.startswith(':'):
            topics_list = [x for x in topics_list if x.startswith(':')]
        else:
            topics_list = [x for x in topics_list if not x.startswith(':')]

        possible_topics = process.extract(topic, topics_list, scorer=fuzz.ratio)[:3]
        possible_topics_text = "\n".join([("    * %s %s" % x) for x in possible_topics])
        return """
Unknown topic.
Do you mean one of these topics maybe?

%s
    """ % possible_topics_text
