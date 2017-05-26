import gevent
from gevent.wsgi import WSGIServer
from gevent.queue import Queue
from gevent.monkey import patch_all
from gevent.subprocess import Popen, PIPE, STDOUT
patch_all()

import sys
import os
import glob
import re
import random
import string

from fuzzywuzzy import process
from fuzzywuzzy import fuzz

import redis
import colored

from pygments import highlight as pygments_highlight
from pygments.lexers import BashLexer, GoLexer, ScalaLexer, RustLexer
from pygments.formatters import TerminalFormatter, Terminal256Formatter

from pygments.styles import get_all_styles
print list(get_all_styles())

MYDIR = os.path.abspath(os.path.dirname(os.path.dirname('__file__')))
sys.path.append("%s/lib/" % MYDIR)
from globals import error, ANSI2HTML, \
                    PATH_TLDR_PAGES, PATH_CHEAT_PAGES, \
                    PATH_CHEAT_SHEETS, PATH_CHEAT_SHEETS_SPOOL

from buttons import TWITTER_BUTTON, GITHUB_BUTTON, GITHUB_BUTTON_2, GITHUB_BUTTON_FOOTER
 
# globals
INTERNAL_TOPICS = [":firstpage", ':post', ':bash_completion', ':help']
LEXER = {
    "go":       GoLexer,
    "scala":    ScalaLexer,
    "rust":     RustLexer,
}
REDIS = redis.StrictRedis(host='localhost', port=6379, db=0)

def update_tldr_topics():
    answer = []
    for topic in glob.glob(PATH_TLDR_PAGES):
        _, filename = os.path.split(topic)
        if filename.endswith('.md'):
            answer.append(filename[:-3])
    return answer
TLDR_TOPICS = update_tldr_topics()

def update_cheat_topics():
    answer = []
    for topic in glob.glob(PATH_CHEAT_PAGES):
        _, filename = os.path.split(topic)
        answer.append(filename)
    return answer
CHEAT_TOPICS = update_cheat_topics()
print CHEAT_TOPICS

def update_cheat_sheets_topics():
    answer = []
    answer_dirs = []

    for topic in glob.glob(PATH_CHEAT_SHEETS + "*/*"):
        dirname, filename = os.path.split(topic)
        answer.append("%s/%s" % (os.path.basename(dirname), filename))
    
    for topic in glob.glob(PATH_CHEAT_SHEETS + "*"):
        _, filename = os.path.split(topic)
        if os.path.isdir(topic):
            answer_dirs.append(filename)
        else:
            answer.append(filename)
    return answer, answer_dirs
CHEAT_SHEETS_TOPICS, CHEAT_SHEETS_DIRS = update_cheat_sheets_topics()


ANSI_ESCAPE = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
def remove_ansi(sometext):
    return ANSI_ESCAPE.sub('', sometext)

def html_wrapper(data):
    p = Popen([ "bash", ANSI2HTML, "--palette=solarized", "--bg=dark" ],  stdin=PIPE, stdout=PIPE, stderr=PIPE)
    data = data.encode('utf-8')
    stdout, stderr = p.communicate(data)
    if p.returncode != 0:
        error(stdout + stderr)
    return stdout.decode('utf-8')

#
#
#

def get_topic_type(topic):
    if topic == "":
        return "search"
    if topic.startswith(":"):
        return "internal"
    if topic in CHEAT_SHEETS_TOPICS:
        return "cheat.sheets"
    if topic.rstrip('/') in CHEAT_SHEETS_DIRS and topic.endswith('/'):
        return "cheat.sheets dir"
    if topic in CHEAT_TOPICS:
        return "cheat"
    if topic in TLDR_TOPICS:
        return "tldr"
    return "unknown"

#
#
#

def get_topics_list(skip_dirs=False, skip_internal=False):
    
    answer = sorted(set(CHEAT_TOPICS + TLDR_TOPICS + CHEAT_SHEETS_TOPICS))
    if not skip_internal:
        answer += INTERNAL_TOPICS
    if not skip_dirs:
        answer += CHEAT_SHEETS_DIRS
    return answer

def get_internal(topic):
    if topic == ":list":
        return "\n".join(x for x in get_topics_list())

    if topic in INTERNAL_TOPICS:
        return open(os.path.join(MYDIR, "share", topic[1:]+".txt"), "r").read()

    return ""

def get_tldr(topic):
    cmd = ["tldr", topic]
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    answer = p.communicate()[0]

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

def get_cheat(topic):
    cmd = ["cheat", topic]
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    answer = p.communicate()[0].decode('utf-8')
    return answer

def get_cheat_sheets(topic):
    return open(PATH_CHEAT_SHEETS + "%s" % topic, "r").read().decode('utf-8')

def get_cheat_sheets_dir(topic):
    answer = []
    for f_name in glob.glob(PATH_CHEAT_SHEETS + "%s/*" % topic.rstrip('/')):
        answer.append(os.path.basename(f_name))
    topics = sorted(answer)
    return "\n".join(topics) + "\n"

def get_unknown(topic):
    topics_list = get_topics_list()
    if topic.startswith(':'):
        topics_list = [x for x in topics_list if x.startswith(':')]
    else:
        topics_list = [x for x in topics_list if not x.startswith(':')]

    possible_topics = process.extract(topic, topics_list, scorer=fuzz.ratio)
    possible_topics = possible_topics[:3]
    possible_topics_text = "\n".join([("    * %s %s" % x) for x in possible_topics])
    return """
Unknown topic.
Do you mean one of these topics may be?

%s
    """ % possible_topics_text

def split_paragraphs(text):
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
        
def paragraph_contains(paragraph, keyword, insensitive=False, word_boundaries=True):
    """
    Several keywords can be joined together using ~
    For example: ~ssh~passphrase
    """
    answer = True

    if '~' in keyword:
        keywords = keyword.split('~')
    else:
        keywords = [keyword]

    for keyword in keywords:
        regex = re.escape(keyword)
        if not word_boundaries:
            regex = r"\b%s\b" % keyword 

        if insensitive:
            answer = answer and bool(re.search(regex, paragraph, re.IGNORECASE))
        else:
            answer = answer and bool(re.search(regex, paragraph))

    return answer

def join_paragraphs(paragraphs):
    answer = "\n".join(paragraphs)
    return answer
    
def get_answer(topic, keyword, options=""):

    answer = None
    if topic != "":
        answer = REDIS.get(topic)
        if answer:
            answer = answer.decode('utf-8')

    if not answer:
        topic_type = get_topic_type(topic)
        if topic_type == "cheat.sheets":
            answer = get_cheat_sheets(topic)
        elif topic_type == "cheat.sheets dir":
            answer = get_cheat_sheets_dir(topic)
        elif topic_type == "tldr":
            answer = get_tldr(topic)
        elif topic_type == "internal":
            answer = get_internal(topic)
            highlight = False
        elif topic_type == "cheat":
            answer = get_cheat(topic)
        else:
            answer = get_unknown(topic)
        if topic_type not in ["search", "internal", "unknown"]:
            REDIS.set(topic, answer)

    if not keyword:
        return answer

    insensitive = 'i' in options
    word_boundaries = 'b' in options

    paragraphs = split_paragraphs(answer)
    paragraphs = [ p for p in paragraphs 
        if paragraph_contains(
            p, keyword, 
            insensitive=insensitive,
            word_boundaries=word_boundaries) ] 
    if len(paragraphs) == 0:
        return ""

    answer = join_paragraphs(paragraphs)
    return answer

def find_answer_by_keyword(directory, keyword, options=""):
    recursive = 'r' in options

    answer_paragraphs = []
    for topic in get_topics_list(skip_internal=True, skip_dirs=True):
        if not topic.startswith(directory):
            continue
        
        subtopic = topic[len(directory):]
        if not recursive and '/' in subtopic:
            continue 

        answer = get_answer(topic, keyword, options=options)
        if answer:
            answer_paragraphs.append((topic, answer))

        MAX_SEARCH_LEN = 20
        if len(answer_paragraphs) > MAX_SEARCH_LEN:
            answer_paragraphs.append(("LIMITED", "LIMITED TO %s ANSWERS" % MAX_SEARCH_LEN))
            break

    return answer_paragraphs

#

def save_cheatsheet(topic_name, cheatsheet):

    nonce = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(9))
    filename = topic_name.replace('/', '.') + "." + nonce
    filename = os.path.join(PATH_CHEAT_SHEETS_SPOOL, filename)

    open(filename, 'w').write(cheatsheet)
#
#
#

def colorize_internal(topic, answer, html_needed):

    def colorize_line(line):
        if line.startswith('T'):
            line = colored.fg("grey_62") + line + colored.attr('reset')
            line = re.sub(r"\{(.*?)\}",  colored.fg("orange_3") + r"\1"+colored.fg('grey_35'), line)
            return line

        line = re.sub(r"\[(F.*?)\]", colored.bg("black") + colored.fg("cyan") + r"[\1]"+colored.attr('reset'), line)
        line = re.sub(r"\[(g.*?)\]", colored.bg("dark_gray") + colored.fg("grey_0") + r"[\1]"+colored.attr('reset'), line)
        line = re.sub(r"\{(.*?)\}",  colored.fg("orange_3") + r"\1"+colored.attr('reset'), line)
        line = re.sub(r"<(.*?)>",    colored.fg("cyan") + r"\1"+colored.attr('reset'), line)
        return line

    if topic in [':list', ':bash_completion']:
        return answer

    if topic == ':firstpage':
        lines = answer.splitlines()
        answer_lines = lines[:9]
        answer_lines.append(colored.fg('grey_35')+lines[9]+colored.attr('reset'))
        for line in lines[10:]:
            answer_lines.append(colorize_line(line))
        if html_needed:
            answer_lines = answer_lines[:-2]
        answer = "\n".join(answer_lines) + "\n"

    return answer

def github_button(topic_type):
    repository = {
        "cheat.sheets":         'chubin/cheat.sheets',
        "cheat.sheets dir":     'chubin/cheat.sheets',
        "tldr":                 'tldr-pages/tldr',
        "internal":             '',
        "cheat":                'chrisallenlane/cheat',
        "search":               '',
        "internal":             '',
        "unknown":              '',
    }

    full_name = repository.get(topic_type, '')
    if not full_name:
        return ''

    short_name = full_name.split('/',1)[1]
    button = (
        "<!-- Place this tag where you want the button to render. -->"
        '<a aria-label="Star %(full_name)s on GitHub" data-count-aria-label="# stargazers on GitHub"'
        ' data-count-api="/repos/%(full_name)s#stargazers_count"'
        ' data-count-href="/%(full_name)s/stargazers"'
        ' data-icon="octicon-star"' 
        ' href="https://github.com/%(full_name)s"'
        '  class="github-button">%(short_name)s</a>'
    ) % locals()
    return button

#

def cheat_wrapper(query, request_options=None, html=False):

    highlight = not bool(request_options and request_options.get('no-terminal'))

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

        answers = find_answer_by_keyword(topic, keyword, options=options)
        search_mode = True
    else:
        answers = [(query, get_answer(query, keyword))]
        search_mode = False


    found = True            # if the page was found in the database
    editable = False        # can generated page be edited on github (only cheat.sheets pages can)
    result = ""
    for topic, answer in answers:
        
        if topic == 'LIMITED':
            result += colored.bg('dark_goldenrod') + colored.fg('yellow_1') + ' ' +  answer + ' ' + colored.attr('reset') + "\n"
            break

        if topic in [":list", ":bash_completion"]:
            highlight = False

        topic_type = get_topic_type(topic)
        if topic_type == 'unknown':
            found = False

        if highlight:
            if topic_type.endswith(" dir"):
                pass
            if topic_type == "unknown":
                # rrt = light green comments
                answer = pygments_highlight(answer, BashLexer(), Terminal256Formatter(style='native'))
            elif topic_type == "internal":
                answer = colorize_internal(topic, answer, html)
            else:
                for lexer_name, lexer in LEXER.items():
                    if topic.startswith("%s/" % lexer_name):
                        answer = pygments_highlight(
                            answer,
                            lexer(),
                            Terminal256Formatter(style='monokai'))
                        break
                else:
                    answer = pygments_highlight(answer, BashLexer(), Terminal256Formatter(style='native'))

        if topic_type == "cheat.sheets":
            editable = True

        if search_mode:
            if highlight:
                result += "\n%s%s %s %s%s\n" % (colored.bg('dark_gray'), colored.attr("res_underlined"), topic, colored.attr("res_underlined"), colored.attr('reset'))
            else: 
                result += "[%s]" % topic

        result += answer

    if search_mode:
        result = result[1:]
        editable = False
        repository_button = ''
    else:
        repository_button = github_button(topic_type)

    if html:
        result = result + "\n$"
        result = html_wrapper(result)
        title = "<title>cheat.sh/%s</title>" % topic
        # title += '\n<link rel="stylesheet" href="/files/awesomplete.css" />script src="/files/awesomplete.min.js" async></script>'
        # submit button: thanks to http://stackoverflow.com/questions/477691/
        submit_button = '<input type="submit" style="position: absolute; left: -9999px; width: 1px; height: 1px;" tabindex="-1" />'
        topic_list = """
<datalist id="topics">%s
</datalist>
        """ % ("\n".join("<option value='%s'></option>" % x for x in get_topics_list()))

        curl_line = "<span class='pre'>$ curl cheat.sh/</span>"
        if query == ':firstpage':
            query = ""
        form_html = '<form action="/" method="GET"/>%s%s<input type="text" value="%s" name="topic" list="topics" autofocus autocomplete="off"/>%s</form>' % (submit_button, curl_line, query, topic_list)

        edit_button = ''
        if editable:
            edit_page_link = 'https://github.com/chubin/cheat.sheets/edit/master/sheets/' + topic
            edit_button = '<pre style="position:absolute;padding-left:40em;overflow:visible;height:0;">[<a href="%s" style="color:cyan">edit</a>]</pre>' % edit_page_link
        result = re.sub("<pre>", edit_button + form_html + "<pre>", result)
        result = re.sub("<head>", "<head>" + title, result)
        if not request_options.get('quiet'):
            result = result.replace('</body>', TWITTER_BUTTON + GITHUB_BUTTON + repository_button + GITHUB_BUTTON_FOOTER + '</body>')

    return result, found

