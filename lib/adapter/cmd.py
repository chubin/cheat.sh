from gevent.monkey import patch_all
from gevent.subprocess import Popen, PIPE
patch_all()

import sys
import abc
import os
import glob
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from globals import PATH_TLDR_PAGES, PATH_CHEAT_PAGES
from adapter import Adapter

def _get_filenames(path):
    return [os.path.split(topic)[1] for topic in glob.glob(path)]

class Tldr(Adapter):

    _adapter_name = "tldr"
    _output_format = "code"
    _cache_needed = True

    def _get_list(self, prefix=None):
        return [filename[:-3]
                for filename in _get_filenames(PATH_TLDR_PAGES) if filename.endswith('.md')]

    def _get_page(self, topic, request_options=None):
        cmd = ["tldr", topic]
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
        answer = proc.communicate()[0]

        fixed_answer = []
        for line in answer.splitlines():
            line = line[2:]
            if line.startswith('-'):
                line = '# '+line[2:]
            elif not line.startswith(' '):
                line = "# "+line
            else:
                pass

            fixed_answer.append(line)

        answer = "\n".join(fixed_answer) + "\n"
        return answer.decode('utf-8')

class Cheat(Adapter):

    _adapter_name = "cheat"
    _output_format = "code"
    _cache_needed = True

    def _get_list(self, prefix=None):
        return _get_filenames(PATH_CHEAT_PAGES)

    def _get_page(self, topic, request_options=None):
        cmd = ["cheat", topic]
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
        answer = proc.communicate()[0].decode('utf-8')
        return answer

class Fosdem(Adapter):

    _adapter_name = "fosdem"
    _output_format = "ansi"

    def _get_list(self, prefix=None):
        return ['fosdem']

    def _get_page(self, topic, request_options=None):
        cmd = ["sudo", "/usr/local/bin/current-fosdem-slide"]
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
        answer = proc.communicate()[0].decode('utf-8')
        return answer

class Translation(Adapter):

    _adapter_name = "translation"
    _output_format = "text"
    _cache_needed = True

    def _get_list(self, prefix=None):
        return []

    def _get_page(self, topic, request_options=None):
        from_, topic = topic.split('/', 1)
        to_ = request_options.get('lang', 'en')
        if '-' in from_:
            from_, to_ = from_.split('-', 1)

        cmd = ["/home/igor/cheat.sh/bin/get_translation",
            from_, to_, topic.replace('+', ' ')]
        print("calling:", cmd)
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
        answer = proc.communicate()[0].decode('utf-8')
        return answer
