"""
Very naive search implementation. Just a placeholder.

Exports:

    find_answer_by_keyword()

It should be implemented on the adapter basis:

    1. adapter.search(keyword) returns list of matching answers
        * maybe with some initial weight
    2. ranking is done
    3. sorted results are returned
    4. eage page are cut by keyword
    5. results are paginated

Configuration parameters:

    search.limit
"""

from config import CONFIG
from routing import get_answer_dict, get_topics_list

def _limited_entry():
    return {
        'topic_type': 'LIMITED',
        "topic": "LIMITED",
        'answer': "LIMITED TO %s ANSWERS" % CONFIG['search.limit'],
        'format': "code",
    }

def find_answers_by_keyword(directory, keyword, options="", request_options=None):
    """
    Search in the whole tree of all cheatsheets or in its subtree `directory`
    by `keyword`
    """

    recursive = 'r' in options

    answers_found = []
    for topic in get_topics_list(skip_internal=True, skip_dirs=True):

        if not topic.startswith(directory):
            continue

        subtopic = topic[len(directory):]
        if not recursive and '/' in subtopic:
            continue

        answer = get_answer_dict(topic, request_options=request_options)

        if answer and answer.get('answer') and keyword.lower() in answer.get('answer', '').lower():
            answers_found.append(answer)

        if len(answers_found) > CONFIG['search.limit']:
            answers_found.append(
                _limited_entry()
            )
            break

    return answers_found
