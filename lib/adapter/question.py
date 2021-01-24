"""
Configuration parameters:

    path.internal.bin.upstream
"""

# pylint: disable=relative-import

from __future__ import print_function

import os
import re
from subprocess import Popen, PIPE

from polyglot.detect import Detector
from polyglot.detect.base import UnknownLanguage

from config import CONFIG
from languages_data import SO_NAME
from .upstream import UpstreamAdapter

NOT_FOUND_MESSAGE = """404 NOT FOUND

Unknown cheat sheet. Please try to reformulate your query.
Query format:

    /LANG/QUESTION

Examples:

    /python/read+json
    /golang/run+external+program
    /js/regex+search

See /:help for more info.

If the problem persists, file a GitHub issue at
github.com/chubin/cheat.sh or ping @igor_chubin
"""

class Question(UpstreamAdapter):

    """
    Answer to a programming language question, using Stackoverflow
    as the main data source. Heavy lifting is done by an external
    program `CONFIG["path.internal.bin.upstream"]`.

    If the program is not found, fallback to the superclass `UpstreamAdapter`,
    which queries the upstream server (by default https://cheat.sh/)
    for the answer
    """

    _adapter_name = "question"
    _output_format = "text+code"
    _cache_needed = True

    def _get_page(self, topic, request_options=None):
        """
        Find answer for the `topic` question.
        """

        if not os.path.exists(CONFIG["path.internal.bin.upstream"]):
            # if the upstream program is not found, use normal upstream adapter
            self._output_format = "ansi"
            return UpstreamAdapter._get_page(self, topic, request_options=request_options)

        topic = topic.replace('+', ' ')

        # if there is a language name in the section name,
        # cut it off (de:python => python)
        if '/' in topic:
            section_name, topic = topic.split('/', 1)
            if ':' in section_name:
                _, section_name = section_name.split(':', 1)
            section_name = SO_NAME.get(section_name, section_name)
            topic = "%s/%s" % (section_name, topic)

        # some clients send queries with - instead of + so we have to rewrite them to
        topic = re.sub(r"(?<!-)-", ' ', topic)

        topic_words = topic.split()

        topic = " ".join(topic_words)

        lang = 'en'
        try:
            query_text = topic # " ".join(topic)
            query_text = re.sub('^[^/]*/+', '', query_text.rstrip('/'))
            query_text = re.sub('/[0-9]+$', '', query_text)
            query_text = re.sub('/[0-9]+$', '', query_text)
            detector = Detector(query_text)
            supposed_lang = detector.languages[0].code
            if len(topic_words) > 2 \
                or supposed_lang in ['az', 'ru', 'uk', 'de', 'fr', 'es', 'it', 'nl']:
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

        cmd = [CONFIG["path.internal.bin.upstream"]] + topic
        proc = Popen(cmd, stdin=open(os.devnull, "r"), stdout=PIPE, stderr=PIPE)
        answer = proc.communicate()[0].decode('utf-8')

        if not answer:
            return NOT_FOUND_MESSAGE

        return answer

    def get_list(self, prefix=None):
        return []

    def is_found(self, topic):
        return True
