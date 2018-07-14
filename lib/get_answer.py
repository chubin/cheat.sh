"""
Main module, answers hub.

Exports:

    get_topics_list()
    get_topic_type()
    get_answer()
"""
from __future__ import print_function

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
from langdetect import detect
from polyglot.detect import Detector
from polyglot.detect.base import UnknownLanguage
import time

import beautifier
from globals import MYDIR, PATH_TLDR_PAGES, PATH_CHEAT_PAGES, PATH_CHEAT_SHEETS, COLOR_STYLES
from adapter_learnxiny import get_learnxiny, get_learnxiny_list, is_valid_learnxy
from languages_data import LANGUAGE_ALIAS, SO_NAME
from colorize_internal import colorize_internal
# pylint: enable=wrong-import-position,wrong-import-order

REDIS = redis.StrictRedis(host='localhost', port=6379, db=0)

MAX_SEARCH_LEN = 20

INTERNAL_TOPICS = [
    ':cht.sh',
    ':bash_completion',
    ':emacs',
    ':emacs-ivy',
    ":firstpage",
    ":firstpage-v1",
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

def _get_filenames(path):
    return [os.path.split(topic)[1] for topic in glob.glob(path)]

def _update_tldr_topics():
    return [ filename[:-3] for filename in _get_filenames(PATH_TLDR_PAGES) if filename.endswith('.md') ]

def _update_cheat_topics():
    return _get_filenames(PATH_CHEAT_PAGES)



TLDR_TOPICS = _update_tldr_topics()
CHEAT_TOPICS = _update_cheat_topics()

def _remove_initial_underscore(filename):
    if filename.startswith('_'):
        filename = filename[1:]
    return filename

def _sanitize_dirname(dirname):
    dirname = os.path.basename(dirname)
    dirname = remove_initial_underscore(dirname)
    return dirname

def _format_answer(dirname,filename):
    return "%s/%s" % ( _sanitize_dirname(dirname), filename )

def _get_answer_files_from_folder():
    topics = map(os.path.split, glob.glob(PATH_CHEAT_SHEETS + "*/*"))
    return [_format_answer(dirname,filename) for dirname, filename in topics if filename not in ['_info.yaml'] ]
def _isdir(topic):
    return os.path.isdir(topic)
def _get_answers_and_dirs():
    topics = glob.glob(PATH_CHEAT_SHEETS + "*")
    answer_dirs = [_remove_initial_underscore(os.path.split(topic)[1]) for topic in topics if _isdir(topic)]
    answers = [ os.path.split(topic)[1] for topic in topics if not _isdir(topic)]
    return answer_dirs, answers

def _update_cheat_sheets_topics():
    answers = _get_answer_files_from_folder()
    cheatsheet_answers, cheatsheet_dirs = _get_answers_and_dirs()
    return answers+cheatsheet_answers, cheatsheet_dirs

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

TOPIC_TYPE_CACHE = {}
def get_topic_type(topic): # pylint: disable=too-many-locals,too-many-branches,too-many-statements
    """
    Return topic type for `topic` or "unknown" if topic can't be determined.
    """
    if topic in TOPIC_TYPE_CACHE:
        return TOPIC_TYPE_CACHE[topic]

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
            else:
		# let us activate the 'question' feature for all subsections
                result = 'question'

    if result == 'unknown' or result == 'question':
        if topic in CHEAT_SHEETS_TOPICS:
            result = "cheat.sheets"
        elif topic.rstrip('/') in CHEAT_SHEETS_DIRS and topic.endswith('/'):
            result = "cheat.sheets dir"
        elif topic in CHEAT_TOPICS:
            result = "cheat"
        elif topic in TLDR_TOPICS:
            result = "tldr"
        elif '/' not in topic:
            result = "unknown"

    TOPIC_TYPE_CACHE[topic] = result

    #print topic, " ", result
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
        if topic[1:] == 'intro':
            return colorize_internal(open(os.path.join(MYDIR, "share", topic[1:]+".txt"), "r").read())
        else:
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
    It's possible that topic directory starts with omitted underscore
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

    topic_words = topic.replace('+', ' ').strip().split()
    topic = " ".join(topic_words)

    lang = 'en'
    try:
        query_text = topic # " ".join(topic)
        query_text = re.sub('^[^/]*/+', '', query_text.rstrip('/'))
        query_text = re.sub('/[0-9]+$', '', query_text)
        query_text = re.sub('/[0-9]+$', '', query_text)
        detector = Detector(query_text)
        print("query_text = ", query_text)
        supposed_lang = detector.languages[0].code
        print("supposed lang = ", supposed_lang)
        if len(topic_words) > 2 or supposed_lang in ['az', 'ru', 'uk', 'de', 'fr', 'es', 'it']:
            lang = supposed_lang
        if supposed_lang.startswith('zh_') or supposed_lang == 'zh':
            lang = 'zh'
        elif supposed_lang.startswith('pt_'):
            lang = 'pt'
        if supposed_lang in ['ja', 'ko']:
            lang = supposed_lang

    except UnknownLanguage:
        print("Unknown language (%s)" % query_text)

    if lang != 'en':
        topic = ['--human-language', lang, topic]
    else:
        topic = [topic]

    cmd = ["/home/igor/cheat.sh/bin/get-answer-for-question"] + topic
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
        print("%s/%s" % (section_name, rest))
        return "%s/%s" % (section_name, rest)


    answer = None
    needs_beautification = False

    topic = _rewrite_aliases(topic)
    topic = _rewrite_section_name(topic)

    # this is pretty unoptimal
    # so this part should be rewritten
    # for the most queries we could say immediately
    # what type the query has
    start_time = time.time()
    topic_type = get_topic_type(topic)
    print((time.time() - start_time)*1000)

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

        answer = REDIS.get(topic)
        if answer:
            answer = answer.decode('utf-8')

    # if answer was not found in the cache
    # try to find it in one of the repositories
    if not answer:
        #topic_type = get_topic_type(topic)

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
