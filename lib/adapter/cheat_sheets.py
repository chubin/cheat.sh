import sys
import os
import glob

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from globals import PATH_CHEAT_SHEETS

def _remove_initial_underscore(filename):
    if filename.startswith('_'):
        filename = filename[1:]
    return filename

def _sanitize_dirname(dirname):
    dirname = os.path.basename(dirname)
    dirname = _remove_initial_underscore(dirname)
    return dirname

def _format_answer(dirname, filename):
    return "%s/%s" % (_sanitize_dirname(dirname), filename)

def _get_answer_files_from_folder():
    topics = map(os.path.split, glob.glob(PATH_CHEAT_SHEETS + "*/*"))
    return [_format_answer(dirname, filename)
            for dirname, filename in topics if filename not in ['_info.yaml']]
def _isdir(topic):
    return os.path.isdir(topic)
def _get_answers_and_dirs():
    topics = glob.glob(PATH_CHEAT_SHEETS + "*")
    answer_dirs = [_remove_initial_underscore(os.path.split(topic)[1]).rstrip('/')+'/'
                   for topic in topics if _isdir(topic)]
    answers = [os.path.split(topic)[1] for topic in topics if not _isdir(topic)]
    return answers, answer_dirs

def _update_cheat_sheets_topics():
    answers = _get_answer_files_from_folder()
    cheatsheet_answers, cheatsheet_dirs = _get_answers_and_dirs()
    return answers+cheatsheet_answers, cheatsheet_dirs

def get_list():
    return _update_cheat_sheets_topics()[0]

def get_dirs_list():
    return _update_cheat_sheets_topics()[1]

_CHEAT_SHEETS_LIST = get_list()
def is_found(topic):
    return topic in _CHEAT_SHEETS_LIST

_CHEAT_SHEETS_DIRS = get_dirs_list()
def is_dir_found(topic):
    return topic in _CHEAT_SHEETS_DIRS

def get_page(topic, request_options=None):
    """
    Get the cheat sheet topic from the own repository (cheat.sheets).
    It's possible that topic directory starts with omitted underscore
    """
    filename = PATH_CHEAT_SHEETS + "%s" % topic
    if not os.path.exists(filename):
        filename = PATH_CHEAT_SHEETS + "_%s" % topic
    if os.path.isdir(filename):
        return ""
    else:
        return open(filename, "r").read().decode('utf-8')

def get_dir(topic, request_options=None):
    answer = []
    for f_name in glob.glob(PATH_CHEAT_SHEETS + "%s/*" % topic.rstrip('/')):
        answer.append(os.path.basename(f_name))
    topics = sorted(answer)
    return "\n".join(topics) + "\n"
