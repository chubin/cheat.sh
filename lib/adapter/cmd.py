from gevent.monkey import patch_all
from gevent.subprocess import Popen, PIPE
patch_all()

import sys
import os
import glob
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from globals import PATH_TLDR_PAGES, PATH_CHEAT_PAGES

def _get_filenames(path):
    return [os.path.split(topic)[1] for topic in glob.glob(path)]

def get_tldr_list():
    return [filename[:-3]
            for filename in _get_filenames(PATH_TLDR_PAGES) if filename.endswith('.md')]

_TLDR_LIST = get_tldr_list()
def tldr_is_found(topic):
    return topic in _TLDR_LIST

def get_tldr(topic, request_options=None):
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

def get_cheat_list():
    return _get_filenames(PATH_CHEAT_PAGES)

_CHEAT_LIST = get_cheat_list()
def cheat_is_found(topic):
    return topic in _CHEAT_LIST

def get_cheat(topic, request_options=None):
    cmd = ["cheat", topic]
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    answer = proc.communicate()[0].decode('utf-8')
    return answer

def get_translation(topic, request_options=None):
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
