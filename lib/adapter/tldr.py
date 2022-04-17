"""
Adapter for https://github.com/cheat/cheat

Cheatsheets are located in `pages/*/`
Each cheat sheet is a separate file with extension .md

The pages are formatted with a markdown dialect
"""

# pylint: disable=relative-import,abstract-method

import re
import os

from .git_adapter import GitRepositoryAdapter

class Tldr(GitRepositoryAdapter):

    """
    tldr-pages/tldr adapter
    """

    _adapter_name = "tldr"
    _output_format = "code"
    _cache_needed = True
    _repository_url = "https://github.com/tldr-pages/tldr"
    _cheatsheet_files_prefix = "pages/*/"
    _cheatsheet_files_extension = ".md"

    @staticmethod
    def _format_page(text):
        """
        Trivial tldr Markdown implementation.

        * Header goes until the first empty line after > prefixed lines.
        * code surrounded with `` => code
        * {{var}} => var
        """

        answer = []
        skip_empty = False
        header = 2
        for line in text.splitlines():
            if line.strip() == '':
                if skip_empty and not header:
                    continue
                if header == 1:
                    header = 0
                if header:
                    continue
            else:
                skip_empty = False

            if line.startswith('-'):
                line = '# '+line[2:]
                skip_empty = True
            elif line.startswith('> '):
                if header == 2:
                    header = 1
                line = '# '+line[2:]
                skip_empty = True
            elif line.startswith('`') and line.endswith('`'):
                line = line[1:-1]
                line = re.sub(r'{{(.*?)}}', r'\1', line)

            answer.append(line)

        return "\n".join(answer)

    def _get_page(self, topic, request_options=None):
        """
        Go through pages/{common,linux,osx,sunos,windows}/
        and as soon as anything is found, format and return it.
        """

        search_order = ['common', 'linux', 'osx', 'sunos', 'windows', "android"]
        local_rep = self.local_repository_location()
        ext = self._cheatsheet_files_extension

        filename = None
        for subdir in search_order:
            _filename = os.path.join(
                local_rep, 'pages', subdir, "%s%s" % (topic, ext))
            if os.path.exists(_filename):
                filename = _filename
                break

        if filename:
            answer = self._format_page(open(filename, 'r').read())
        else:
            # though it should not happen
            answer = ''

        return answer

    @classmethod
    def get_updates_list(cls, updated_files_list):
        """
        If a .md file was updated, invalidate cache
        entry with the name of this file
        """
        answer = []
        ext = cls._cheatsheet_files_extension

        for entry in updated_files_list:
            if entry.endswith(ext):
                answer.append(entry.split('/')[-1][:-len(ext)])
        return answer
