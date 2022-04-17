"""
Implementation of `GitRepositoryAdapter`, adapter that is used to handle git repositories
"""

import glob
import os

from .adapter import Adapter # pylint: disable=relative-import

def _get_filenames(path):
    return [os.path.split(topic)[1] for topic in glob.glob(path)]

class RepositoryAdapter(Adapter):
    """
    Implements methods needed to handle standard
    repository based adapters.
    """

    def _get_list(self, prefix=None):
        """
        List of files in the cheat sheets directory
        with the extension removed
        """

        answer = _get_filenames(
            os.path.join(
                self.local_repository_location(),
                self._cheatsheet_files_prefix,
                '*'+self._cheatsheet_files_extension))

        ext = self._cheatsheet_files_extension
        if ext:
            answer = [filename[:-len(ext)]
                      for filename in answer
                      if filename.endswith(ext)]

        return answer

    def _get_page(self, topic, request_options=None):

        filename = os.path.join(
            self.local_repository_location(),
            self._cheatsheet_files_prefix,
            topic)

        if os.path.exists(filename) and not os.path.isdir(filename):
            answer = self._format_page(open(filename, 'r').read())
        else:
            # though it should not happen
            answer = "%s:%s not found" % (str(self.__class__), topic)

        return answer


class GitRepositoryAdapter(RepositoryAdapter):    #pylint: disable=abstract-method
    """
    Implements all methods needed to handle cache handling
    for git-repository-based adapters
    """

    @classmethod
    def fetch_command(cls):
        """
        Initial fetch of the repository.
        Return cmdline that has to be executed to fetch the repository.
        Skipping if `self._repository_url` is not specified
        """

        if not cls._repository_url:
            return None

        if not cls._repository_url.startswith('https://github.com/'):
            # in this case `fetch` has to be implemented
            # in the distinct adapter subclass
            raise RuntimeError(
                "Do not known how to handle this repository: %s" % cls._repository_url)

        local_repository_dir = cls.local_repository_location()
        if not local_repository_dir:
            return None

        return ['git', 'clone', '--depth=1', cls._repository_url, local_repository_dir]

    @classmethod
    def update_command(cls):
        """
        Update of the repository.
        Return cmdline that has to be executed to update the repository
        inside `local_repository_location()`.
        """

        if not cls._repository_url:
            return None

        local_repository_dir = cls.local_repository_location()
        if not local_repository_dir:
            return None

        if not cls._repository_url.startswith('https://github.com/'):
            # in this case `update` has to be implemented
            # in the distinct adapter subclass
            raise RuntimeError(
                "Do not known how to handle this repository: %s" % cls._repository_url)

        return ['git', 'pull']

    @classmethod
    def current_state_command(cls):
        """
        Get current state of repository (current revision).
        This is used to find what cache entries should be invalidated.
        """

        if not cls._repository_url:
            return None

        local_repository_dir = cls.local_repository_location()
        if not local_repository_dir:
            return None

        if not cls._repository_url.startswith('https://github.com/'):
            # in this case `update` has to be implemented
            # in the distinct adapter subclass
            raise RuntimeError(
                "Do not known how to handle this repository: %s" % cls._repository_url)

        return ['git', 'rev-parse', '--short', 'HEAD', "--"]

    @classmethod
    def save_state(cls, state):
        """
        Save state `state` of the repository.
        Must be called after the cache clean up.
        """
        local_repository_dir = cls.local_repository_location()
        state_filename = os.path.join(local_repository_dir, '.cached_revision')
        open(state_filename, 'wb').write(state)

    @classmethod
    def get_state(cls):
        """
        Return the saved `state` of the repository.
        If state cannot be read, return None
        """

        local_repository_dir = cls.local_repository_location()
        state_filename = os.path.join(local_repository_dir, '.cached_revision')
        state = None
        if os.path.exists(state_filename):
            state = open(state_filename, 'r').read()
        return state

    @classmethod
    def get_updates_list_command(cls):
        """
        Return list of updates since the last update whose id is saved as the repository state.
        The list is used to invalidate the cache.
        """
        current_state = cls.get_state()
        if not current_state:
            return ['git', 'ls-tree', '--full-tree', '-r', '--name-only', 'HEAD', "--"]
        return ['git', 'diff', '--name-only', current_state, 'HEAD', "--"]
