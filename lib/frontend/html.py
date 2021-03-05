"""

Configuration parameters:

    path.internal.ansi2html
"""

import sys
import os
import re
from subprocess import Popen, PIPE

MYDIR = os.path.abspath(os.path.join(__file__, '..', '..'))
sys.path.append("%s/lib/" % MYDIR)

# pylint: disable=wrong-import-position
from config import CONFIG
from globals import error
from buttons import TWITTER_BUTTON, GITHUB_BUTTON, GITHUB_BUTTON_FOOTER
import frontend.ansi

# temporary having it here, but actually we have the same data
# in the adapter module
GITHUB_REPOSITORY = {
    "late.nz"           :   'chubin/late.nz',
    "cheat.sheets"      :   'chubin/cheat.sheets',
    "cheat.sheets dir"  :   'chubin/cheat.sheets',
    "tldr"              :   'tldr-pages/tldr',
    "cheat"             :   'chrisallenlane/cheat',
    "learnxiny"         :   'adambard/learnxinyminutes-docs',
    "internal"          :   '',
    "search"            :   '',
    "unknown"           :   '',
}

def visualize(answer_data, request_options):
    query = answer_data['query']
    answers = answer_data['answers']
    topics_list = answer_data['topics_list']
    editable = (len(answers) == 1 and answers[0]['topic_type'] == 'cheat.sheets')

    repository_button = ''
    if len(answers) == 1:
        repository_button = _github_button(answers[0]['topic_type'])

    result, found = frontend.ansi.visualize(answer_data, request_options)
    return _render_html(query, result, editable, repository_button, topics_list, request_options), found

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

def _render_html(query, result, editable, repository_button, topics_list, request_options):

    def _html_wrapper(data):
        """
        Convert ANSI text `data` to HTML
        """
        cmd = ["bash", CONFIG['path.internal.ansi2html'], "--palette=solarized", "--bg=dark"]
        try:
            proc = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        except FileNotFoundError:
            print("ERROR: %s" % cmd)
            raise
        data = data.encode('utf-8')
        stdout, stderr = proc.communicate(data)
        if proc.returncode != 0:
            error((stdout + stderr).decode('utf-8'))
        return stdout.decode('utf-8')


    result = result + "\n$"
    result = _html_wrapper(result)
    title = "<title>cheat.sh/%s</title>" % query
    submit_button = ('<input type="submit" style="position: absolute;'
                     ' left: -9999px; width: 1px; height: 1px;" tabindex="-1" />')
    topic_list = ('<datalist id="topics">%s</datalist>'
                  % ("\n".join("<option value='%s'></option>" % x for x in topics_list)))

    curl_line = "<span class='pre'>$ curl cheat.sh/</span>"
    if query == ':firstpage':
        query = ""
    form_html = ('<form action="/" method="GET">'
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
