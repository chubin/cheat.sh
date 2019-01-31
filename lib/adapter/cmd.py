from gevent.monkey import patch_all
from gevent.subprocess import Popen, PIPE
patch_all()

import sys
import abc
import os
import glob
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from globals import PATH_TLDR_PAGES, PATH_CHEAT_PAGES

def _get_filenames(path):
    return [os.path.split(topic)[1] for topic in glob.glob(path)]

class Cmd(object):
    def __init__(self):
        self._list = self._get_list()

    @abc.abstractmethod
    def _get_list(self):
        return []

    def get_list(self):
        return self._list

    def is_found(self, topic):
        return topic in self._list

    @abc.abstractmethod
    def get_page(self, topic, request_options=None):
        pass

class Tldr(Cmd):
    def _get_list(self):
        return [filename[:-3]
                for filename in _get_filenames(PATH_TLDR_PAGES) if filename.endswith('.md')]

    def get_page(self, topic, request_options=None):
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

class Cheat(Cmd):
    def _get_list(self):
        return _get_filenames(PATH_CHEAT_PAGES)

    def get_page(self, topic, request_options=None):
        cmd = ["cheat", topic]
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
        answer = proc.communicate()[0].decode('utf-8')
        return answer

class Fosdem(Cmd):
    def _get_list(self):
        return ['fosdem']

    def get_page(self, topic, request_options=None):
        cmd = ["sudo", "/home/igor/bin/current-fosdem-slide"]
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
        answer = proc.communicate()[0].decode('utf-8')
        return answer

class Translation(Cmd):
    def _get_list(self):
        return []

    def get_page(self, topic, request_options=None):
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
