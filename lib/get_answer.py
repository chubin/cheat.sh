"""
Main module, answers hub.

Exports:

    get_topics_list()
    get_topic_type()
    get_answer()
"""

from gevent.monkey import patch_all
from gevent.subprocess import Popen, PIPE
patch_all()

# pylint: disable=wrong-import-position,wrong-import-order
import collections
import glob
import os
import re
import redis
from fuzzywuzzy import process, fuzz

import beautifier
from globals import MYDIR, PATH_TLDR_PAGES, PATH_CHEAT_PAGES, PATH_CHEAT_SHEETS, COLOR_STYLES
from adapter_learnxiny import get_learnxiny, get_learnxiny_list, is_valid_learnxy
from languages_data import LANGUAGE_ALIAS, SO_NAME
# pylint: enable=wrong-import-position,wrong-import-order

REDIS = redis.StrictRedis(host='localhost', port=6379, db=0)

MAX_SEARCH_LEN = 20

INTERNAL_TOPICS = [
    ':bash',
    ':bash_completion',
    ':emacs',
    ':emacs-ivy',
    ":firstpage",
    ":firstpage-v2",
    ':fish',
    ':help',
    ":intro",
    ":list",
    ':post',
    ':styles',
    ':styles-demo',
    ':vim',
    ':zsh',
    ':share',
    ]

def _update_tldr_topics():
    answer = []
    for topic in glob.glob(PATH_TLDR_PAGES):
        _, filename = os.path.split(topic)
        if filename.endswith('.md'):
            answer.append(filename[:-3])
    return answer
TLDR_TOPICS = _update_tldr_topics()

def _update_cheat_topics():
    answer = []
    for topic in glob.glob(PATH_CHEAT_PAGES):
        _, filename = os.path.split(topic)
        answer.append(filename)
    return answer
CHEAT_TOPICS = _update_cheat_topics()

def _update_cheat_sheets_topics():
    answer = []
    answer_dirs = []

    for topic in glob.glob(PATH_CHEAT_SHEETS + "*/*"):
        dirname, filename = os.path.split(topic)
        if filename in ['_info.yaml']:
            continue
        dirname = os.path.basename(dirname)
        if dirname.startswith('_'):
            dirname = dirname[1:]
        answer.append("%s/%s" % (dirname, filename))

    for topic in glob.glob(PATH_CHEAT_SHEETS + "*"):
        _, filename = os.path.split(topic)
        if os.path.isdir(topic):
            if filename.startswith('_'):
                filename = filename[1:]
            answer_dirs.append(filename+'/')
        else:
            answer.append(filename)
    return answer, answer_dirs
CHEAT_SHEETS_TOPICS, CHEAT_SHEETS_DIRS = _update_cheat_sheets_topics()

CACHED_TOPICS_LIST = [[]]
def get_topics_list(skip_dirs=False, skip_internal=False):
    """
    List of topics returned on /:list
    """

    if CACHED_TOPICS_LIST[0] != []:
        return CACHED_TOPICS_LIST[0]

    answer = CHEAT_TOPICS + TLDR_TOPICS + CHEAT_SHEETS_TOPICS
    answer = sorted(set(answer))

    # doing it in this strange way to save the order of the topics
    for topic in get_learnxiny_list():
        if topic not in answer:
            answer.append(topic)

    if not skip_dirs:
        answer += CHEAT_SHEETS_DIRS
    if not skip_internal:
        answer += INTERNAL_TOPICS

    CACHED_TOPICS_LIST[0] = answer
    return answer

def _get_topics_dirs():
    return set([x.split('/', 1)[0] for x in get_topics_list() if '/' in x])


def _get_stat():
    stat = collections.Counter([
        get_topic_type(topic) for topic in get_topics_list()
    ])

    answer = ""
    for key, val in stat.items():
        answer += "%s %s\n" % (key, val)
    return answer
#
#
#

def get_topic_type(topic): # pylint: disable=too-many-locals,too-many-branches,too-many-statements
    """
    Return topic type for `topic` or "unknown" if topic can't be determined.
    """
    result = 'unknown'

    if topic == "":
        result = "search"
    elif topic.startswith(":"):
        result = "internal"
    elif '/' in topic:
        topic_type, topic_name = topic.split('/', 1)
        if '+' in topic_name:
            result = 'question'
        else:
            if topic_type in _get_topics_dirs() and topic_name in [':list']:
                result = "internal"
            elif is_valid_learnxy(topic):
                result = 'learnxiny'

    if result == 'unknown':
        if topic in CHEAT_SHEETS_TOPICS:
            result = "cheat.sheets"
        elif topic.rstrip('/') in CHEAT_SHEETS_DIRS and topic.endswith('/'):
            result = "cheat.sheets dir"
        elif topic in CHEAT_TOPICS:
            result = "cheat"
        elif topic in TLDR_TOPICS:
            result = "tldr"
        elif '+' in topic:
            result = "question"

    print topic, " ", result
    return result

#
#   Various cheat sheets getters
#
#
#def registered_answer_getter(func):
#    REGISTERED_ANSWER_GETTERS.append(funct)
#    return cls

def _get_internal(topic):
    if '/' in topic:
        topic_type, topic_name = topic.split('/', 1)
        if topic_name == ":list":
            topic_list = [x[len(topic_type)+1:]
                          for x in get_topics_list()
                          if x.startswith(topic_type + "/")]
            return "\n".join(topic_list)+"\n"

    if topic == ":list":
        return "\n".join(x for x in get_topics_list()) + "\n"

    if topic == ':styles':
        return "\n".join(COLOR_STYLES) + "\n"

    if topic == ":stat":
        return _get_stat()+"\n"

    if topic in INTERNAL_TOPICS:
        return open(os.path.join(MYDIR, "share", topic[1:]+".txt"), "r").read()

    return ""

def _get_tldr(topic):
    cmd = ["tldr", topic]
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    answer = proc.communicate()[0]

    fixed_answer = []
    for line in answer.splitlines():
        line = line[2:]
        if line.startswith('-'):
            line = '# '+line[2:]
        elif line == "":
            pass
        elif not line.startswith(' '):
            line = "# "+line

        fixed_answer.append(line)

    answer = "\n".join(fixed_answer) + "\n"
    return answer.decode('utf-8')

def _get_cheat(topic):
    cmd = ["cheat", topic]
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    answer = proc.communicate()[0].decode('utf-8')
    return answer

def _get_cheat_sheets(topic):
    """
    Get the cheat sheet topic from the own repository (cheat.sheets).
    It's possible that topic directory starts with omited underscore
    """
    filename = PATH_CHEAT_SHEETS + "%s" % topic
    if not os.path.exists(filename):
        filename = PATH_CHEAT_SHEETS + "_%s" % topic
    return open(filename, "r").read().decode('utf-8')

def _get_cheat_sheets_dir(topic):
    answer = []
    for f_name in glob.glob(PATH_CHEAT_SHEETS + "%s/*" % topic.rstrip('/')):
        answer.append(os.path.basename(f_name))
    topics = sorted(answer)
    return "\n".join(topics) + "\n"

def _get_answer_for_question(topic):
    """
    Find answer for the `topic` question.
    """

    topic = " ".join(topic.replace('+', ' ').strip().split())
    cmd = ["/home/igor/cheat.sh/bin/get-answer-for-question", topic]
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    answer = proc.communicate()[0].decode('utf-8')
    return answer

def _get_unknown(topic):
    topics_list = get_topics_list()
    if topic.startswith(':'):
        topics_list = [x for x in topics_list if x.startswith(':')]
    else:
        topics_list = [x for x in topics_list if not x.startswith(':')]

    possible_topics = process.extract(topic, topics_list, scorer=fuzz.ratio)[:3]
    possible_topics_text = "\n".join([("    * %s %s" % x) for x in possible_topics])
    return """
Unknown topic.
Do you mean one of these topics may be?

%s
    """ % possible_topics_text

# pylint: disable=bad-whitespace
#
# topic_type, function_getter
# should be replaced with a decorator
TOPIC_GETTERS = (
    ("cheat.sheets",        _get_cheat_sheets),
    ("cheat.sheets dir",    _get_cheat_sheets_dir),
    ("tldr",                _get_tldr),
    ("internal",            _get_internal),
    ("cheat",               _get_cheat),
    ("learnxiny",           get_learnxiny),
    ("question",            _get_answer_for_question),
    ("unknown",             _get_unknown),
)
# pylint: enable=bad-whitespace

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
        section_name = LANGUAGE_ALIAS.get(section_name, section_name)
        return "%s/%s" % (section_name, rest)

    def _rewrite_section_name_for_q(query):
        """
        """
        if '/' not in query:
            return query

        section_name, rest = query.split('/', 1)
        section_name = SO_NAME.get(section_name, section_name)
        print "%s/%s" % (section_name, rest)
        return "%s/%s" % (section_name, rest)


    answer = None
    needs_beautification = False

    topic = _rewrite_aliases(topic)
    topic = _rewrite_section_name(topic)

    # checking if the answer is in the cache
    if topic != "":
        # temporary hack for "questions":
        # the topic name has to be prefixed with q:
        # so we can later delete them from redis
        # and we known that they need beautification
        if '/' in topic and '+' in topic:
            topic = _rewrite_section_name_for_q(topic)
            topic = "q:" + topic
            needs_beautification = True

        answer = REDIS.get(topic)
        if answer:
            answer = answer.decode('utf-8')

    # if answer was not found in the cache
    # try to find it in one of the repositories
    if not answer:
        topic_type = get_topic_type(topic)

        for topic_getter_type, topic_getter in TOPIC_GETTERS:
            if topic_type == topic_getter_type:
                answer = topic_getter(topic)
                break
        if not answer:
            topic_type = "unknown"
            answer = _get_unknown(topic)

        # saving answers in the cache
        if topic_type not in ["search", "internal", "unknown"]:
            REDIS.set(topic, answer)

    if needs_beautification:
        filetype = 'bash'
        if '/' in topic:
            filetype = topic.split('/', 1)[0]
            if filetype.startswith('q:'):
                filetype = filetype[2:]

        answer = beautifier.beautify(answer.encode('utf-8'), filetype, request_options)

    if not keyword:
        return answer

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
        # skip the internal pages, don't show them in search
        if topic in INTERNAL_TOPICS:
            continue

        if not topic.startswith(directory):
            continue

        subtopic = topic[len(directory):]
        if not recursive and '/' in subtopic:
            continue

        answer = get_answer(topic, keyword, options=options, request_options=request_options)
        if answer:
            answer_paragraphs.append((topic, answer))

        if len(answer_paragraphs) > MAX_SEARCH_LEN:
            answer_paragraphs.append(("LIMITED", "LIMITED TO %s ANSWERS" % MAX_SEARCH_LEN))
            break

    return answer_paragraphs
