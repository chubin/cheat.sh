"""
Main cheat.sh wrapper.
Get answers from getters (in get_answer), adds syntax highlighting
or html markup and returns the result.
"""

from gevent.monkey import patch_all
from gevent.subprocess import Popen, PIPE
patch_all()

# pylint: disable=wrong-import-position,wrong-import-order
import sys
import os
import re

import colored
from pygments import highlight as pygments_highlight
from pygments.formatters import Terminal256Formatter # pylint: disable=no-name-in-module

MYDIR = os.path.abspath(os.path.join(__file__, '..', '..'))
sys.path.append("%s/lib/" % MYDIR)
from globals import error, ANSI2HTML, COLOR_STYLES, GITHUB_REPOSITORY
from buttons import TWITTER_BUTTON, GITHUB_BUTTON, GITHUB_BUTTON_FOOTER
from languages_data import LEXER, get_lexer_name
from get_answer import get_topic_type, get_topics_list, get_answer, find_answer_by_keyword
from beautifier import code_blocks
# import beautifier
# pylint: disable=wrong-import-position,wrong-import-order

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

    if topic == ':firstpage-v1':
        lines = answer.splitlines()
        answer_lines = lines[:9]
        answer_lines.append(colored.fg('grey_35')+lines[9]+colored.attr('reset'))
        for line in lines[10:]:
            answer_lines.append(_colorize_line(line))
        if html_needed:
            answer_lines = answer_lines[:-2]
        answer = "\n".join(answer_lines) + "\n"

    return answer

def _colorize_ansi_answer(topic, answer, color_style,               # pylint: disable=too-many-arguments
                          highlight_all=True, highlight_code=False,
                          unindent_code=False):

    color_style = color_style or "native"
    lexer_class = LEXER['bash']
    if '/' in topic:
        section_name = topic.split('/', 1)[0].lower()
        section_name = get_lexer_name(section_name)
        lexer_class = LEXER.get(section_name, lexer_class)
        if section_name == 'php':
            answer = "<?\n%s?>\n" % answer

    if highlight_all:
        highlight = lambda answer: pygments_highlight(
            answer, lexer_class(), Terminal256Formatter(style=color_style)).strip('\n')+'\n'
    else:
        highlight = lambda x: x

    if highlight_code:
        blocks = code_blocks(answer, wrap_lines=True, unindent_code=(4 if unindent_code else False))
        highlighted_blocks = []
        for block in blocks:
            if block[0] == 1:
                this_block = highlight(block[1])
            else:
                this_block = block[1].strip('\n')+'\n'
            highlighted_blocks.append(this_block)

        result = "\n".join(highlighted_blocks)
    else:
        result = highlight(answer).lstrip('\n')
    return result

def _github_button(topic_type):

    full_name = GITHUB_REPOSITORY.get(topic_type, '')
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

def _render_html(query, result, editable, repository_button, request_options):

    result = result + "\n$"
    result = html_wrapper(result)
    title = "<title>cheat.sh/%s</title>" % query
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
        # It's possible that topic directory starts with omitted underscore
        if '/' in query:
            query = '_' + query
        edit_page_link = 'https://github.com/chubin/cheat.sheets/edit/master/sheets/' + query
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
    return result

def _visualize(query, keyword, answers, request_options, html=None): # pylint: disable=too-many-locals

    search_mode = bool(keyword)

    highlight = not bool(request_options and request_options.get('no-terminal'))
    color_style = request_options.get('style', '')
    if color_style not in COLOR_STYLES:
        color_style = ''

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

        topic_type = get_topic_type(topic)
        highlight = (highlight
                     and topic not in [":list", ":bash_completion"]
                     and topic_type not in ["unknown"]
                    )
        found = found and not topic_type == 'unknown'
        editable = editable or topic_type == "cheat.sheets"

        if topic_type == "internal" and highlight:
            answer = _colorize_internal(topic, answer, html)
        elif topic_type in ["late.nz", "fosdem"]:
            pass
        else:
            answer = _colorize_ansi_answer(
                topic, answer, color_style,
                highlight_all=highlight,
                highlight_code=(topic_type == 'question'
                                and not request_options.get('add_comments')
                                and not request_options.get('remove_text')),
                unindent_code=request_options.get('unindent_code')
                )

        if search_mode:
            if not highlight:
                result += "\n[%s]\n" % topic
            else:
                result += "\n%s%s %s %s%s\n" % (colored.bg('dark_gray'),
                                                colored.attr("res_underlined"),
                                                topic,
                                                colored.attr("res_underlined"),
                                                colored.attr('reset'))
        result += answer

    result = result.strip('\n') + "\n"

    if search_mode:
        editable = False
        repository_button = ''
    else:
        repository_button = _github_button(topic_type)

    if html and query:
        result = _render_html(
            query, result, editable, repository_button, request_options)


    return result, found

def _sanitize_query(query):
    return re.sub('[<>"]', '', query)

def cheat_wrapper(query, request_options=None, html=False):
    """
    Giant megafunction that delivers cheat sheet for `query`.
    If `html` is True, the answer is formatted as HTML.
    Additional request options specified in `request_options`.

    This function is really really bad, and should be rewritten
    as soon as possible.
    """

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
        answers = [(topic, get_answer(topic, keyword, request_options=request_options))]

    return _visualize(query, keyword, answers, request_options, html=html)
