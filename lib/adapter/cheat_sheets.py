"""
Implementation of the adapter for the native cheat.sh cheat sheets repository,
cheat.sheets.  The cheat sheets repository is hierarchically structured: cheat
sheets covering programming languages are are located in subdirectories.
"""

# pylint: disable=relative-import

import os
import glob

from .git_adapter import GitRepositoryAdapter

def _remove_initial_underscore(filename):
    if filename.startswith('_'):
        filename = filename[1:]
    return filename

def _sanitize_dirnames(filename, restore=False):
    """
    Remove (or add) leading _ in the directories names in `filename`
    The `restore` param means that the path name should be restored from the queryname,
    i.e. conversion should be done in the opposite direction
    """
    parts = filename.split('/')
    newparts = []
    for part in parts[:-1]:
        if restore:
            newparts.append('_'+part)
            continue
        if part.startswith('_'):
            newparts.append(part[1:])
        else:
            newparts.append(part)
    newparts.append(parts[-1])

    return "/".join(newparts)

class CheatSheets(GitRepositoryAdapter):

    """
    Adapter for the cheat.sheets cheat sheets.
    """

    _adapter_name = "cheat.sheets"
    _output_format = "code"
    _repository_url = "https://github.com/chubin/cheat.sheets"
    _cheatsheet_files_prefix = "sheets/"

    def _get_list(self, prefix=None):
        """
        Return all files on the first and the second level,
        excluding directories and hidden files
        """

        hidden_files = ["_info.yaml"]
        answer = []
        prefix = os.path.join(
            self.local_repository_location(),
            self._cheatsheet_files_prefix)
        for mask in ['*', '*/*']:
            template = os.path.join(
                prefix,
                mask)

            answer += [
                _sanitize_dirnames(f_name[len(prefix):])
                for f_name in glob.glob(template)
                if not os.path.isdir(f_name)
                and os.path.basename(f_name) not in hidden_files]

        return sorted(answer)

    def _get_page(self, topic, request_options=None):

        filename = os.path.join(
            self.local_repository_location(),
            self._cheatsheet_files_prefix,
            _sanitize_dirnames(topic, restore=True))

        if os.path.exists(filename):
            answer = self._format_page(open(filename, 'r').read())
        else:
            # though it should not happen
            answer = "%s:%s not found" % (str(self.__class__), topic)

        return answer

class CheatSheetsDir(CheatSheets):

    """
    Adapter for the cheat sheets directories.
    Provides pages named according to subdirectories:
        _dir => dir/

    (currently only _get_list() is used; _get_page is shadowed
    by the CheatSheets adapter)
    """

    _adapter_name = "cheat.sheets dir"
    _output_format = "text"

    def _get_list(self, prefix=None):

        template = os.path.join(
            self.local_repository_location(),
            self._cheatsheet_files_prefix,
            '*')

        answer = sorted([
            _remove_initial_underscore(os.path.basename(f_name)) + "/"
            for f_name in glob.glob(template)
            if os.path.isdir(f_name)])

        return answer

    def _get_page(self, topic, request_options=None):
        """
        Content of the `topic` dir is the list of the pages in the dir
        """

        template = os.path.join(
            self.local_repository_location(),
            self._cheatsheet_files_prefix,
            topic.rstrip('/'),
            '*')

        answer = sorted([
            os.path.basename(f_name) for f_name in glob.glob(template)])
        return "\n".join(answer) + "\n"

    def is_found(self, topic):
        return CheatSheets.is_found(self, topic.rstrip('/'))
