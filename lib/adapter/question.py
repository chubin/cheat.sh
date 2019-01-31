from gevent.monkey import patch_all
from gevent.subprocess import Popen, PIPE
patch_all()

import sys
import os
import re

from polyglot.detect import Detector
from polyglot.detect.base import UnknownLanguage

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from globals import MYDIR

def get_page(topic, request_options=None):
    """
    Find answer for the `topic` question.
    """

    # if there is a language name in the section name,
    # cut it off (de:python => python)
    if '/' in topic:
        section_name, topic = topic.split('/', 1)
        if ':' in section_name:
            _, section_name = section_name.split(':', 1)
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
        if len(topic_words) > 2 or supposed_lang in ['az', 'ru', 'uk', 'de', 'fr', 'es', 'it', 'nl']:
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

    cmd = [os.path.join(MYDIR, "bin/get-answer-for-question")] + topic
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    answer = proc.communicate()[0].decode('utf-8')
    return answer
