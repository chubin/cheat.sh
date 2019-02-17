"""
Main module, answers hub.

Exports:

    get_topics_list()
    get_answer()
    find_answer_by_keyword()
"""
from __future__ import print_function

import os
import re
import redis

from globals import REDISHOST, MAX_SEARCH_LEN
from languages_data import LANGUAGE_ALIAS, SO_NAME, rewrite_editor_section_name

import fmt.comments

import cache
import adapter.cheat_sheets
import adapter.cmd
import adapter.internal
import adapter.latenz
import adapter.learnxiny
import adapter.question
import adapter.rosetta

class Router(object):

    """
    Implementation of query routing.
    Routing is done basing on the data exported by the adapters.
    (mainly by functions get_list() and is_found()).

    Function get_topics_list() returns available topics
    (that are accessible at /:list).

    Function get_topic_type() delivers name of the adapter,
    that will process the query.
    """

    def __init__(self):

        self._cached_topics_list = []
        self._cached_topic_type = {}

        self._adapter = {
            "internal": adapter.internal.InternalPages(
                get_topic_type=self.get_topic_type,
                get_topics_list=self.get_topics_list),
            "unknown": adapter.internal.UnknownPages(
                get_topic_type=self.get_topic_type,
                get_topics_list=self.get_topics_list),
            "tldr": adapter.cmd.Tldr(),
            "cheat": adapter.cmd.Cheat(),
            "fosdem": adapter.cmd.Fosdem(),
            "translation": adapter.cmd.Translation(),
            "rosetta": adapter.rosetta.Rosetta(),
            "late.nz": adapter.latenz.Latenz(),
            "question": adapter.question.Question(),
            "cheat.sheets": adapter.cheat_sheets.CheatSheets(),
            "cheat.sheets dir": adapter.cheat_sheets.CheatSheetsDir(),
            "learnxiny": adapter.learnxiny.LearnXinY(),
        }

        self._topic_list = {
            key: obj.get_list()
            for key, obj in self._adapter.items()
        }

    def get_topics_list(self, skip_dirs=False, skip_internal=False):
        """
        List of topics returned on /:list
        """

        if self._cached_topics_list:
            return self._cached_topics_list

        sources_to_merge = ['tldr', 'cheat', 'cheat.sheets', 'learnxiny', 'rosetta']
        if not skip_dirs:
            sources_to_merge.append("cheat.sheets dir")
        if not skip_internal:
            sources_to_merge.append("internal")

        answer = {}
        for key in sources_to_merge:
            answer.update({name:key for name in self._topic_list[key]})
        answer = sorted(set(answer.keys()))

        self._cached_topics_list = answer
        return answer

    def get_topic_type(self, topic):
        """
        Return topic type for `topic` or "unknown" if topic can't be determined.
        """

        def __get_topic_type(topic):

            routing_table = [
                ("^$", "search"),
                ("^[^/]*/rosetta(/|$)", "rosetta"),
                ("^:", "internal"),
                ("/:list$", "internal"),
                ("/$", "cheat.sheets dir"),
                ("", "cheat.sheets"),
                ("", "cheat"),
                ("", "tldr"),
                ("", "late.nz"),
                ("", "fosdem"),
                ("^[/]*$", "unknown"),
                ("", "learnxiny"),
                ("^[a-z][a-z]-[a-z][a-z]$", "translation"),
            ]

            for regexp, route in routing_table:
                if re.search(regexp, topic):
                    if route in self._adapter:
                        if self._adapter[route].is_found(topic):
                            return route
                    else:
                        return route

            return 'question'

        if topic not in self._cached_topic_type:
            self._cached_topic_type[topic] = __get_topic_type(topic)
        return self._cached_topic_type[topic]

    def get_page_dict(self, query, request_options=None):
        """
        Return answer_dict for the `query`.
        """

        topic_type = self.get_topic_type(query)
        return self._adapter[topic_type]\
               .get_page_dict(query, request_options=request_options)

if os.environ.get('REDIS_HOST', '').lower() != 'none':
    REDIS = redis.StrictRedis(host=REDISHOST, port=6379, db=0)
else:
    REDIS = None

_ROUTER = Router()
get_topics_list = _ROUTER.get_topics_list

def get_answer(topic, keyword, options="", request_options=None): # pylint: disable=too-many-locals,too-many-branches,too-many-statements
    """
    Find cheat sheet for the topic.
    If `keyword` is None or rempty, return the whole answer.
    Otherwise cut the paragraphs containing keywords.

    Args:
        topic (str):    the name of the topic of the cheat sheet
        keyword (str):  the name of the keywords to search in the cheat sheets

    Returns:
        string:         the cheat sheet
    """

    def _join_paragraphs(paragraphs):
        answer = "\n".join(paragraphs)
        return answer

    def _split_paragraphs(text):
        answer = []
        paragraph = ""
        for line in text.splitlines():
            if line == "":
                answer.append(paragraph)
                paragraph = ""
            else:
                paragraph += line+"\n"
        answer.append(paragraph)
        return answer

    def _paragraph_contains(paragraph, keyword, insensitive=False, word_boundaries=True):
        """
        Check if `paragraph` contains `keyword`.
        Several keywords can be joined together using ~
        For example: ~ssh~passphrase
        """
        answer = True

        if '~' in keyword:
            keywords = keyword.split('~')
        else:
            keywords = [keyword]

        for kwrd in keywords:
            regex = re.escape(kwrd)
            if not word_boundaries:
                regex = r"\b%s\b" % kwrd

            if insensitive:
                answer = answer and bool(re.search(regex, paragraph, re.IGNORECASE))
            else:
                answer = answer and bool(re.search(regex, paragraph))

        return answer

    def _rewrite_aliases(word):
        if word == ':bash.completion':
            return ':bash_completion'
        return word

    def _rewrite_section_name(query):
        """
        """
        if '/' not in query:
            return query

        section_name, rest = query.split('/', 1)

        if ':' in section_name:
            # if ':' is in section_name, it means, that we want to
            # translate the answer in the specified human language
            # (experimental)
            language, section_name = section_name.split(':', 1)
        else:
            language = ""

        section_name = LANGUAGE_ALIAS.get(section_name, section_name)

        if language:
            section_name = language + ":" + section_name

        return "%s/%s" % (section_name, rest)

    def _rewrite_section_name_for_q(query):
        """
        FIXME: we rewrite the section name too earlier,
        what means that we have to use SO names everywhere,
        where actually canonified internal names shoud be used.
        After this thing is fixed, we should:
        * fix naming in cache
        * fix VIM_NAMES
        """
        if '/' not in query:
            return query

        section_name, rest = query.split('/', 1)
        if ':' in section_name:
            section_name = rewrite_editor_section_name(section_name)

        section_name = SO_NAME.get(section_name, section_name)
        return "%s/%s" % (section_name, rest)


    answer = None
    needs_beautification = False

    topic = _rewrite_aliases(topic)
    topic = _rewrite_section_name(topic)

    # This is pretty unoptimal, so this part should be rewritten.
    # For the most queries we could say immediately, # what type the query has.
    topic_type = _ROUTER.get_topic_type(topic)

    # Checking if the answer is in the cache
    if topic != "":
        # Temporary hack for "questions": # the topic name has to be prefixed with `q:`
        # so we can later delete them from REDIS.
        # And we known that they need beautification
        if topic_type == 'question':
            topic = _rewrite_section_name_for_q(topic)
            topic = "q:" + topic
            needs_beautification = True

        if REDIS:
            answer = REDIS.get(topic)
        if answer:
            answer = answer.decode('utf-8')

    # If answer was not found in the cache, try to find it in one of the repositories
    if not answer:
        answer = _ROUTER.get_page_dict(topic, request_options=request_options)

        # saving answers in the cache
        if REDIS:
            if answer and answer['topic_type'] not in ["search", "internal", "unknown"]:
                REDIS.set(topic, answer)

    if needs_beautification:
        filetype = 'bash'
        if '/' in topic:
            filetype = topic.split('/', 1)[0]
            if filetype.startswith('q:'):
                filetype = filetype[2:]

        answer['answer'] = fmt.comments.beautify(
            answer['answer'].encode('utf-8'), filetype, request_options)

    if not keyword:
        return answer

# pylint: disable=invalid-name
_ROUTER = Router()
get_topics_list = _ROUTER.get_topics_list
get_answer_dict = _ROUTER.get_answer_dict
