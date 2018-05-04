"""
Main cheat.sh wrapper.
Gets answer from the getters, add syntax highlighting or html markup and returns it.
At the moment, it contains the getters that should be moved out to a separate file.
"""

from gevent.monkey import patch_all
from gevent.subprocess import Popen, PIPE
patch_all()

# pylint: disable=wrong-import-position,wrong-import-order
import sys
import os
import glob
import re
import random
import string
import collections

import colored
import redis
from fuzzywuzzy import process, fuzz

from pygments import highlight as pygments_highlight
from pygments.formatters import Terminal256Formatter # pylint: disable=no-name-in-module
from pygments.styles import get_all_styles

MYDIR = os.path.abspath(os.path.dirname(os.path.dirname('__file__')))
sys.path.append("%s/lib/" % MYDIR)
from globals import error, ANSI2HTML, \
                    PATH_TLDR_PAGES, PATH_CHEAT_PAGES, \
                    PATH_CHEAT_SHEETS, PATH_CHEAT_SHEETS_SPOOL
from buttons import TWITTER_BUTTON, GITHUB_BUTTON, GITHUB_BUTTON_FOOTER
from adapter_learnxiny import get_learnxiny, get_learnxiny_list, is_valid_learnxy
from languages_data import LEXER, LANGUAGE_ALIAS
import beautifier
# pylint: disable=wrong-import-position,wrong-import-order

COLOR_STYLES = sorted(list(get_all_styles()))

# globals
INTERNAL_TOPICS = [
    ":list",
    ":firstpage",
    ':post',
    ':bash_completion',
    ':help',
    ':styles',
    ':styles-demo',
    ':emacs',
    ':emacs-ivy',
    ':fish',
    ':bash',
    ':zsh'
    ]


REDIS = redis.StrictRedis(host='localhost', port=6379, db=0)
MAX_SEARCH_LEN = 20

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

ANSI_ESCAPE = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
def remove_ansi(sometext):
    """
    Remove ANSI sequences from `sometext` and convert it into plaintext.
    """
    return ANSI_ESCAPE.sub('', sometext)

def html_wrapper(data):
    """
    Convert ANSI text `data` to HTML
    """
    proc = Popen(
        ["bash", ANSI2HTML, "--palette=solarized", "--bg=dark"],
        stdin=PIPE, stdout=PIPE, stderr=PIPE)
    data = data.encode('utf-8')
    stdout, stderr = proc.communicate(data)
    if proc.returncode != 0:
        error(stdout + stderr)
    return stdout.decode('utf-8')

#
#
#

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
    result = ''
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
                result = 'question'

    elif topic in CHEAT_SHEETS_TOPICS:
        result = "cheat.sheets"
    elif topic.rstrip('/') in CHEAT_SHEETS_DIRS and topic.endswith('/'):
        result = "cheat.sheets dir"
    elif topic in CHEAT_TOPICS:
        result = "cheat"
    elif topic in TLDR_TOPICS:
        result = "tldr"
    elif '+' in topic:
        result = "question"
    else:
        result = 'unknown'
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

    answer = None
    needs_beautification = False

    # checking if the answer is in the cache
    if topic != "":
        # temporary hack for "questions":
        # the topic name has to be prefixed with q:
        # so we can later delete them from redis
        # and we known that they need beautification
        if '/' in topic and '+' in topic:
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

#
#========================>8   cut here  8<===================================================
#

def save_cheatsheet(topic_name, cheatsheet):
    """
    Save posted cheat sheet `cheatsheet` with `topic_name`
    in the spool directory
    """

    nonce = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(9))
    filename = topic_name.replace('/', '.') + "." + nonce
    filename = os.path.join(PATH_CHEAT_SHEETS_SPOOL, filename)

    open(filename, 'w').write(cheatsheet)
#
#
#

def _colorize_internal(topic, answer, html_needed):

    def _colorize_line(line):
        if line.startswith('T'):
            line = colored.fg("grey_62") + line + colored.attr('reset')
            line = re.sub(r"\{(.*?)\}", colored.fg("orange_3") + r"\1"+colored.fg('grey_35'), line)
            return line

        line = re.sub(r"\[(F.*?)\]",
                      colored.bg("black") + colored.fg("cyan") + r"[\1]"+colored.attr('reset'),
                      line)
        line = re.sub(r"\[(g.*?)\]",
                      colored.bg("dark_gray") \
                      + colored.fg("grey_0") \
                      + r"[\1]"+colored.attr('reset'),
                      line)
        line = re.sub(r"\{(.*?)\}",
                      colored.fg("orange_3") + r"\1"+colored.attr('reset'),
                      line)
        line = re.sub(r"<(.*?)>",
                      colored.fg("cyan") + r"\1"+colored.attr('reset'),
                      line)
        return line

    if topic in [':list', ':bash_completion']:
        return answer

    if topic == ':firstpage':
        lines = answer.splitlines()
        answer_lines = lines[:9]
        answer_lines.append(colored.fg('grey_35')+lines[9]+colored.attr('reset'))
        for line in lines[10:]:
            answer_lines.append(_colorize_line(line))
        if html_needed:
            answer_lines = answer_lines[:-2]
        answer = "\n".join(answer_lines) + "\n"

    return answer

def _github_button(topic_type):

    repository = {
        "cheat.sheets"      :   'chubin/cheat.sheets',
        "cheat.sheets dir"  :   'chubin/cheat.sheets',
        "tldr"              :   'tldr-pages/tldr',
        "cheat"             :   'chrisallenlane/cheat',
        "learnxiny"         :   'adambard/learnxinyminutes-docs',
        "internal"          :   '',
        "search"            :   '',
        "unknown"           :   '',
    }

    full_name = repository.get(topic_type, '')
    if not full_name:
        return ''

    short_name = full_name.split('/', 1)[1] # pylint: disable=unused-variable

    button = (
        "<!-- Place this tag where you want the button to render. -->"
        '<a aria-label="Star %(full_name)s on GitHub"'
        ' data-count-aria-label="# stargazers on GitHub"'
        ' data-count-api="/repos/%(full_name)s#stargazers_count"'
        ' data-count-href="/%(full_name)s/stargazers"'
        ' data-icon="octicon-star"'
        ' href="https://github.com/%(full_name)s"'
        '  class="github-button">%(short_name)s</a>'
    ) % locals()
    return button

#

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

def cheat_wrapper(query, request_options=None, html=False): # pylint: disable=too-many-locals,too-many-branches,too-many-statements
    """
    Giant megafunction that delivers cheat sheet for `query`.
    If `html` is True, the answer is formated as HTML.
    Additional request options specified in `request_options`.

    This function is really really bad, and should be rewritten
    as soon as possible.
    """

    #
    # at the moment, we just remove trailing slashes
    # so queries python/ and python are equal
    #
    query = query.rstrip('/')

    query = _rewrite_aliases(query)
    query = _rewrite_section_name(query)

    highlight = not bool(request_options and request_options.get('no-terminal'))
    color_style = request_options.get('style', '')
    if color_style not in COLOR_STYLES:
        color_style = ''

    keyword = None
    if '~' in query:
        topic = query
        pos = topic.index('~')
        keyword = topic[pos+1:]
        topic = topic[:pos]

        options = ""
        if '/' in keyword:
            options = keyword[::-1]
            options = options[:options.index('/')]
            keyword = keyword[:-len(options)-1]

        answers = find_answer_by_keyword(
            topic, keyword, options=options, request_options=request_options)
        search_mode = True
    else:
        answers = [(query, get_answer(query, keyword, request_options=request_options))]
        search_mode = False


    found = True            # if the page was found in the database
    editable = False        # can generated page be edited on github (only cheat.sheets pages can)
    result = ""
    for topic, answer in answers:   # pylint: disable=too-many-nested-blocks

        if topic == 'LIMITED':
            result += colored.bg('dark_goldenrod') \
                    + colored.fg('yellow_1') \
                    + ' ' +  answer + ' ' \
                    + colored.attr('reset') + "\n"
            break

        if topic in [":list", ":bash_completion"]:
            highlight = False

        topic_type = get_topic_type(topic)
        if topic_type == 'unknown':
            found = False

        if highlight:
            #if topic_type.endswith(" dir"):
            #    pass

            if topic_type == "internal":
                answer = _colorize_internal(topic, answer, html)
            else:
                color_style = color_style or "native"
                lexer = LEXER['bash']
                for lexer_name, lexer_value in LEXER.items():
                    if topic.startswith('cpp'):
                        topic = 'c++' + topic[3:]

                    if topic.startswith("%s/" % lexer_name):
                        color_style = color_style or "monokai"
                        if lexer_name == 'php':
                            answer = "<?\n%s?>\n" % answer
                        lexer = lexer_value
                        break

                formatter = Terminal256Formatter(style=color_style)
                answer = pygments_highlight(answer, lexer(), formatter).lstrip('\n')

        if topic_type == "cheat.sheets":
            editable = True

        if search_mode:
            if highlight:
                result += "\n%s%s %s %s%s\n" % (colored.bg('dark_gray'),
                                                colored.attr("res_underlined"),
                                                topic,
                                                colored.attr("res_underlined"),
                                                colored.attr('reset'))
            else:
                result += "\n[%s]\n" % topic

        result += answer

    if search_mode:
        result = result[1:]
        editable = False
        repository_button = ''
    else:
        repository_button = _github_button(topic_type)

    if html:
        result = result + "\n$"
        result = html_wrapper(result)
        title = "<title>cheat.sh/%s</title>" % topic
        # title += ('\n<link rel="stylesheet" href="/files/awesomplete.css" />script'
        #           ' src="/files/awesomplete.min.js" async></script>')
        # submit button: thanks to http://stackoverflow.com/questions/477691/
        submit_button = ('<input type="submit" style="position: absolute;'
                         ' left: -9999px; width: 1px; height: 1px;" tabindex="-1" />')
        topic_list = ('<datalist id="topics">%s</datalist>'
                      % ("\n".join("<option value='%s'></option>" % x for x in get_topics_list())))

        curl_line = "<span class='pre'>$ curl cheat.sh/</span>"
        if query == ':firstpage':
            query = ""
        form_html = ('<form action="/" method="GET"/>'
                     '%s%s'
                     '<input'
                     ' type="text" value="%s" name="topic"'
                     ' list="topics" autofocus autocomplete="off"/>'
                     '%s'
                     '</form>') \
                     % (submit_button, curl_line, query, topic_list)

        edit_button = ''
        if editable:
            # It's possible that topic directory starts with omited underscore
            if '/' in topic:
                topic = '_' + topic
            edit_page_link = 'https://github.com/chubin/cheat.sheets/edit/master/sheets/' + topic
            edit_button = (
                '<pre style="position:absolute;padding-left:40em;overflow:visible;height:0;">'
                '[<a href="%s" style="color:cyan">edit</a>]'
                '</pre>') % edit_page_link
        result = re.sub("<pre>", edit_button + form_html + "<pre>", result)
        result = re.sub("<head>", "<head>" + title, result)
        if not request_options.get('quiet'):
            result = result.replace('</body>',
                                    TWITTER_BUTTON \
                                    + GITHUB_BUTTON \
                                    + repository_button \
                                    + GITHUB_BUTTON_FOOTER \
                                    + '</body>')

    return result, found
