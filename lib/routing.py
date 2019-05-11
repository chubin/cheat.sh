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
from config import CONFIG

class Router(object):

    """
    Implementation of query routing. Routing is based on `routing_table`
    and the data exported by the adapters (functions `get_list()` and `is_found()`).

    `get_topics_list()` returns available topics (accessible at /:list).
    `get_answer_dict()` return answer for the query.
    """

    def __init__(self):

        self._cached_topics_list = []
        self._cached_topic_type = {}

        adapter_class = adapter.all_adapters(as_dict=True)

        active_adapters = set(CONFIG['adapters.active'] + CONFIG['adapters.mandatory'])

        self._adapter = {
            "internal": adapter.internal.InternalPages(
                get_topic_type=self.get_topic_type,
                get_topics_list=self.get_topics_list),
            "unknown": adapter.internal.UnknownPages(
                get_topic_type=self.get_topic_type,
                get_topics_list=self.get_topics_list),
        }

        for by_name in active_adapters:
            if by_name not in self._adapter:
                self._adapter[by_name] = adapter_class[by_name]()

        self._topic_list = {
            key: obj.get_list()
            for key, obj in self._adapter.items()
        }

        self.routing_table = CONFIG["routing.main"]
        self.routing_table = CONFIG["routing.pre"] + self.routing_table + CONFIG["routing.post"]

    def get_topics_list(self, skip_dirs=False, skip_internal=False):
        """
        List of topics returned on /:list
        """

        if self._cached_topics_list:
            return self._cached_topics_list

        skip = ['fosdem']
        if skip_dirs:
            skip.append("cheat.sheets dir")
        if skip_internal:
            skip.append("internal")
        sources_to_merge = [x for x in self._adapter if x not in skip]

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
            return CONFIG["routing.default"]

        if topic not in self._cached_topic_type:
            self._cached_topic_type[topic] = __get_topic_type(topic)
        return self._cached_topic_type[topic]

    def _get_page_dict(self, query, topic_type, request_options=None):
        """
        Return answer_dict for the `query`.
        """

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

            answer = self._get_page_dict(topic, topic_type, request_options=request_options)
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

        answer = self._get_page_dict(topic, topic_type, request_options=request_options)
        if isinstance(answer, dict):
            if "cache" in answer:
                cache_needed = answer["cache"]

        if cache_needed and answer:
            cache.put(topic, answer)
        return answer

# pylint: disable=invalid-name
_ROUTER = Router()
get_topics_list = _ROUTER.get_topics_list
get_answer_dict = _ROUTER.get_answer_dict
