"""
Queries routing and caching.

Exports:

    get_topics_list()
    get_answer_dict()
"""
from __future__ import print_function

import re

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
    Implementation of query routing. Routing is based on `routing_table`
    and the data exported by the adapters (functions `get_list()` and `is_found()`).

    `get_topics_list()` returns available topics (accessible at /:list).
    `get_answer_dict()` return answer for the query.
    """

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
        ("^[^/]*$", "unknown"),
        ("", "learnxiny"),
        ("^[a-z][a-z]-[a-z][a-z]$", "translation"),
    ]

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
            "search": adapter.internal.Search(),
            "tldr": adapter.tldr.Tldr(),
            "cheat": adapter.cheat_cheat.Cheat(),
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

            for regexp, route in self.routing_table:
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

    def _get_page_dict(self, query, request_options=None):
        """
        Return answer_dict for the `query`.
        """

        topic_type = self.get_topic_type(query)
        return self._adapter[topic_type]\
               .get_page_dict(query, request_options=request_options)

    def get_answer_dict(self, topic, request_options=None):
        """
        Find cheat sheet for the topic.

        Args:
            `topic` (str):    the name of the topic of the cheat sheet

        Returns:
            answer_dict:      the answer dictionary
        """

        topic_type = self.get_topic_type(topic)

        # 'question' queries are pretty expensive, that's why they should be handled
        # in a special way:
        # we do not drop the old style cache entries and try to reuse them if possible
        if topic_type == 'question':
            answer = cache.get('q:' + topic)
            if answer:
                if isinstance(answer, dict):
                    return answer
                return {
                    'topic': topic,
                    'topic_type': 'question',
                    'answer': answer,
                    'format': 'text+code',
                    }

            answer = self._get_page_dict(topic, request_options=request_options)
            cache.put('q:' + topic, answer)
            return answer

        # Try to find cacheable queries in the cache.
        # If answer was not found in the cache, resolve it in a normal way and save in the cache
        cache_needed = self._adapter[topic_type].is_cache_needed()
        if cache_needed:
            answer = cache.get(topic)
            if not isinstance(answer, dict):
                answer = None
            if answer:
                return answer

        answer = self._get_page_dict(topic, request_options=request_options)

        if cache_needed and answer:
            cache.put(topic, answer)
        return answer

# pylint: disable=invalid-name
_ROUTER = Router()
get_topics_list = _ROUTER.get_topics_list
get_answer_dict = _ROUTER.get_answer_dict
