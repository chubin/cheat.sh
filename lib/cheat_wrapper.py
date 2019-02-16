"""
Main cheat.sh wrapper.
Parse the query, get answers from getters (using get_answer),
visualize it using frontends and return the result.

Exports:

    cheat_wrapper()
"""

import re
import json

from get_answer import get_answer, find_answer_by_keyword, get_topics_list
import frontend.html
import frontend.ansi

def cheat_wrapper(query, request_options=None, output_format='ansi'):
    """
    Function that delivers cheat sheet for `query`.
    If `html` is True, the answer is formatted as HTML.
    Additional request options specified in `request_options`.
    """

    def _sanitize_query(query):
        return re.sub('[<>"]', '', query)

    def _strip_hyperlink(query):
        return re.sub('(,[0-9]+)+$', '', query)

    def _parse_query(query):
        topic = query
        keyword = None
        search_options = ""

        keyword = None
        if '~' in query:
            topic = query
            pos = topic.index('~')
            keyword = topic[pos+1:]
            topic = topic[:pos]

            if '/' in keyword:
                search_options = keyword[::-1]
                search_options = search_options[:search_options.index('/')]
                keyword = keyword[:-len(search_options)-1]

        return topic, keyword, search_options

    query = _sanitize_query(query)

    # at the moment, we just remove trailing slashes
    # so queries python/ and python are equal
    query = _strip_hyperlink(query.rstrip('/'))
    topic, keyword, search_options = _parse_query(query)

    if keyword:
        answers = find_answer_by_keyword(
            topic, keyword, options=search_options, request_options=request_options)
    else:
        answers = [get_answer(topic, keyword, request_options=request_options)]

    answer_data = {
        'query': query,
        'keyword': keyword,
        'answers': answers,
        }

    if output_format == 'html':
        answer_data['topics_list'] = get_topics_list()
        return frontend.html.visualize(answer_data, request_options)
    elif output_format == 'json':
        return json.dumps(answer_data, indent=4)
    return frontend.ansi.visualize(answer_data, request_options)
