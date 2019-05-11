"""
Implementation of RosettaCode Adapter.

Exports:

    Rosetta(GitRepositoryAdapter)
"""

# pylint: disable=relative-import

import os
import glob
import yaml

from .git_adapter import GitRepositoryAdapter
from .cheat_sheets import CheatSheets

class Rosetta(GitRepositoryAdapter):

    """
    Adapter for RosettaCode
    """

    _adapter_name = "rosetta"
    _output_format = "code"
    _local_repository_location = "RosettaCodeData"
    _repository_url = "https://github.com/acmeism/RosettaCodeData"

    __section_name = "rosetta"

    def __init__(self):
        GitRepositoryAdapter.__init__(self)
        self._rosetta_code_name = self._load_rosetta_code_names()

    @staticmethod
    def _load_rosetta_code_names():
        answer = {}

        lang_files_location = CheatSheets.local_repository_location(cheat_sheets_location=True)
        for filename in glob.glob(os.path.join(lang_files_location, '*/_info.yaml')):
            text = open(filename, 'r').read()
            data = yaml.load(text, Loader=yaml.SafeLoader)
            if data is None:
                continue
            lang = os.path.basename(os.path.dirname(filename))
            if lang.startswith('_'):
                lang = lang[1:]
            if 'rosetta' in data:
                answer[lang] = data['rosetta']
        return answer

    def _rosetta_get_list(self, query, task=None):
        if query not in self._rosetta_code_name:
            return []

        lang = self._rosetta_code_name[query]
        answer = []
        if task:
            glob_path = os.path.join(self.local_repository_location(), 'Lang', lang, task, '*')
        else:
            glob_path = os.path.join(self.local_repository_location(), 'Lang', lang, '*')
        for filename in glob.glob(glob_path):
            taskname = os.path.basename(filename)
            answer.append(taskname)

        answer = "".join("%s\n" % x for x in sorted(answer))
        return answer

    @staticmethod
    def _parse_query(query):
        if '/' in query:
            task, subquery = query.split('/', 1)
        else:
            task, subquery = query, None
        return task, subquery

    def _get_task(self, lang, query):
        if lang not in self._rosetta_code_name:
            return ""

        task, subquery = self._parse_query(query)

        if task == ':list':
            return self._rosetta_get_list(lang)
        if subquery == ':list':
            return self._rosetta_get_list(lang, task=task)

        # if it is not a number or the number is too big, just ignore it
        index = 1
        if subquery:
            try:
                index = int(subquery)
            except ValueError:
                pass

        lang_name = self._rosetta_code_name[lang]

        tasks = sorted(glob.glob(
            os.path.join(self.local_repository_location(), 'Lang', lang_name, task, '*')))
        if not tasks:
            return ""

        if len(tasks) < index or index < 1:
            index = 1

        answer_filename = tasks[index-1]
        answer = open(answer_filename, 'r').read()

        return answer

    def _starting_page(self, query):
        number_of_pages = self._rosetta_get_list(query)
        answer = (
            "# %s pages available\n"
            "# use /:list to list"
        ) % number_of_pages
        return answer

    def _get_page(self, topic, request_options=None):

        if '/' not in topic:
            return self._rosetta_get_list(topic)

        lang, topic = topic.split('/', 1)

        # this part should be generalized
        # currently we just remove the name of the adapter from the path
        if topic == self.__section_name:
            return self._starting_page(topic)

        if topic.startswith(self.__section_name + '/'):
            topic = topic[len(self.__section_name + '/'):]

        return self._get_task(lang, topic)

    def _get_list(self, prefix=None):
        return []

    def get_list(self, prefix=None):
        answer = [self.__section_name]
        for i in self._rosetta_code_name:
            answer.append('%s/%s/' % (i, self.__section_name))
        return answer

    def is_found(self, _):
        return True
