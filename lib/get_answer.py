"""
Main module, answers hub.

Exports:

    get_topics_list()
    get_topic_type()
    get_answer()
    find_answer_by_keyword()
"""
from __future__ import print_function

import os
import re
import redis

import beautifier
from globals import REDISHOST, MAX_SEARCH_LEN
from languages_data import LANGUAGE_ALIAS, SO_NAME, rewrite_editor_section_name

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

    Refactoring of the class is almost done.
    The next steps to do:
    * _topic_list, _topic_found and topic_getters should be merged together.
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

        self._topic_found = {
            key: obj.is_found
            for key, obj in self._adapter.items()
        }

# topic_type, function_getter
# should be replaced with a decorator
# pylint: disable=bad-whitespace
        self.topic_getters = (
            ("cheat.sheets",        self._adapter["cheat.sheets"].get_page_dict),
            ("cheat.sheets dir",    self._adapter["cheat.sheets dir"].get_page_dict),
            ("learnxiny",           self._adapter["learnxiny"].get_page_dict),
            ("question",            self._adapter["question"].get_page_dict),
            ("fosdem",              self._adapter["fosdem"].get_page_dict),
            ("late.nz",             self._adapter["late.nz"].get_page_dict),
            ("rosetta",             self._adapter["rosetta"].get_page_dict),
            ("tldr",                self._adapter["tldr"].get_page_dict),
            ("internal",            self._adapter["internal"].get_page_dict),
            ("cheat",               self._adapter["cheat"].get_page_dict),
            ("translation",         self._adapter["translation"].get_page_dict),
            ("unknown",             self._adapter["unknown"].get_page_dict),
        )
# pylint: enable=bad-whitespace

    def get_topics_list(self, skip_dirs=False, skip_internal=False):
        """
        List of topics returned on /:list
        """

        if self._cached_topics_list:
            return self._cached_topics_list

        # merging all top level lists
        sources_to_merge = ['tldr', 'cheat', 'cheat.sheets', 'learnxiny', 'rosetta']
        if not skip_dirs:
            sources_to_merge.append("cheat.sheets dir")
        if not skip_internal:
            sources_to_merge.append("internal")

        answer = {}
        for key in sources_to_merge:
            answer.update({name:key for name in self._topic_list[key]})
        answer = sorted(set(answer.keys()))

        # # doing it in this strange way to save the order of the topics
        # for topic in adapter.learnxiny.get_learnxiny_list():
        #     if topic not in answer:
        #         answer.append(topic)

        self._cached_topics_list = answer
        return answer

    def get_topic_type(self, topic): # pylint: disable=too-many-locals,too-many-branches,too-many-statements
        """
        Return topic type for `topic` or "unknown" if topic can't be determined.
        """

        def __get_topic_type(topic):

            if topic == "":
                return "search"
            if re.match('[^/]*/rosetta(/|$)', topic):
                return "rosetta"
            if topic.startswith(":"):
                return "internal"
            if topic.endswith("/:list"):
                return "internal"
            if topic.endswith('/'):
                topic = topic.rstrip('/')
                if self._topic_found['cheat.sheets dir'](topic):
                    return "cheat.sheets dir"

            for source in ['cheat.sheets', 'cheat', 'tldr', 'late.nz', 'fosdem']:
                if self._topic_found[source](topic):
                    return source

            if '/' not in topic:
                #if '+' in topic_name:
                #    return 'question'
                return "unknown"

            # topic contains '/'
            #
            if self._adapter['learnxiny'].is_found(topic):
                return 'learnxiny'
            topic_type = topic.split('/', 1)[0]
            if topic_type in ['ru', 'fr'] or re.match(r'[a-z][a-z]-[a-z][a-z]$', topic_type):
                return 'translation'
            return 'question'

        if topic not in self._cached_topic_type:
            self._cached_topic_type[topic] = __get_topic_type(topic)
        return self._cached_topic_type[topic]

if os.environ.get('REDIS_HOST', '').lower() != 'none':
    REDIS = redis.StrictRedis(host=REDISHOST, port=6379, db=0)
else:
    REDIS = None

_ROUTER = Router()

get_topic_type = _ROUTER.get_topic_type
get_topics_list = _ROUTER.get_topics_list
TOPIC_GETTERS = _ROUTER.topic_getters

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

    # this is pretty unoptimal
    # so this part should be rewritten
    # for the most queries we could say immediately
    # what type the query has
    topic_type = get_topic_type(topic)

    # checking if the answer is in the cache
    if topic != "":
        # temporary hack for "questions":
        # the topic name has to be prefixed with q:
        # so we can later delete them from redis
        # and we known that they need beautification
        #if '/' in topic and '+' in topic:
        if topic_type == 'question': #'/' in topic and '+' in topic:
            topic = _rewrite_section_name_for_q(topic)
            topic = "q:" + topic
            needs_beautification = True

        if REDIS:
            answer = REDIS.get(topic)
        if answer:
            answer = answer.decode('utf-8')

    # if answer was not found in the cache
    # try to find it in one of the repositories
    if not answer:

        for topic_getter_type, topic_getter in TOPIC_GETTERS:
            if topic_type == topic_getter_type:
                answer = topic_getter(topic, request_options=request_options)
                break
        if not answer:
            topic_type = "unknown"
            answer = dict(TOPIC_GETTERS)['unknown'](topic)

        # saving answers in the cache
        if REDIS:
            if topic_type not in ["search", "internal", "unknown"]:
                REDIS.set(topic, answer)

    if needs_beautification:
        filetype = 'bash'
        if '/' in topic:
            filetype = topic.split('/', 1)[0]
            if filetype.startswith('q:'):
                filetype = filetype[2:]

        answer['answer'] = beautifier.beautify(answer['answer'].encode('utf-8'), filetype, request_options)

    # if isinstance(answer, str):
    #     answer_dict = {
    #         'topic': topic,
    #         'topic_type': topic_type,
    #         'answer':   answer,
    #         'format': 'code',
    #         }
    # else:
    answer_dict = answer

    if not keyword:
        return answer_dict

    #
    # shorten the answer, because keyword is specified
    #
    insensitive = 'i' in options
    word_boundaries = 'b' in options

    paragraphs = _split_paragraphs(answer)
    paragraphs = [p for p in paragraphs
                  if _paragraph_contains(p, keyword,
                                         insensitive=insensitive,
                                         word_boundaries=word_boundaries)]
    if paragraphs == []:
        return ""

    answer = _join_paragraphs(paragraphs)

    return answer

def find_answer_by_keyword(directory, keyword, options="", request_options=None):
    """
    Search in the whole tree of all cheatsheets or in its subtree `directory`
    by `keyword`
    """

    recursive = 'r' in options

    answer_paragraphs = []
    for topic in get_topics_list(skip_internal=True, skip_dirs=True):

        if not topic.startswith(directory):
            continue

        subtopic = topic[len(directory):]
        if not recursive and '/' in subtopic:
            continue

        answer = get_answer(topic, keyword, options=options, request_options=request_options)
        if answer:
            answer_paragraphs.append(answer)

        if len(answer_paragraphs) > MAX_SEARCH_LEN:
            answer_paragraphs.append({
                'topic_type': 'LIMITED',
                'answer': "LIMITED TO %s ANSWERS" % MAX_SEARCH_LEN,
            })
            break

    return answer_paragraphs
