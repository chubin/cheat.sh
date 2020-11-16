"""
`Adapter`, base class of the adapters.

Configuration parameters:

    path.repositories
"""

import abc
import os
from six import with_metaclass
from config import CONFIG

class AdapterMC(type):
    """
    Adapter Metaclass.
    Defines string representation of adapters
    """
    def __repr__(cls):
        if hasattr(cls, '_class_repr'):
            return getattr(cls, '_class_repr')()
        return super(AdapterMC, cls).__repr__()

class Adapter(with_metaclass(AdapterMC, object)):
    """
    An abstract class, defines methods:

    (cheat sheets retrieval)
    * get_list
    * is_found
    * is_cache_needed

    (repositories management)
    " fetch
    * update

    and several properties that have to be set in each adapter subclass.

    """

    _adapter_name = None
    _output_format = 'code'
    _cache_needed = False
    _repository_url = None
    _local_repository_location = None
    _cheatsheet_files_prefix = ""
    _cheatsheet_files_extension = ""
    _pages_list = []

    @classmethod
    def _class_repr(cls):
        return '[Adapter: %s (%s)]' % (cls._adapter_name, cls.__name__)

    def __init__(self):
        self._list = {None: self._get_list()}

    @classmethod
    def name(cls):
        """
        Return name of the adapter
        """
        return cls._adapter_name

    @abc.abstractmethod
    def _get_list(self, prefix=None):
        return self._pages_list

    def get_list(self, prefix=None):
        """
        Return available pages for `prefix`
        """

        if prefix in self._list:
            return self._list[prefix]

        self._list[prefix] = set(self._get_list(prefix=prefix))
        return self._list[prefix]

    def is_found(self, topic):
        """
        check if `topic` is available
        CAUTION: only root is checked
        """
        return topic in self._list[None]

    def is_cache_needed(self):
        """
        Return True if answers should be cached.
        Return False if answers should not be cached.
        """
        return self._cache_needed

    @staticmethod
    def _format_page(text):
        """
        Preformatting page hook.
        Converts `text` (as in the initial repository)
        to text (as to be displayed).
        """

        return text

    @abc.abstractmethod
    def _get_page(self, topic, request_options=None):
        """
        Return page for `topic`
        """
        pass

    def _get_output_format(self, topic):
        if '/' in topic:
            subquery = topic.split('/')[-1]
        else:
            subquery = topic

        if subquery in [':list']:
            return 'text'
        return self._output_format

    # pylint: disable=unused-argument
    @staticmethod
    def _get_filetype(topic):
        """
        Return language name (filetype) for `topic`
        """
        return None

    def get_page_dict(self, topic, request_options=None):
        """
        Return page dict for `topic`
        """

        #
        # if _get_page() returns a dict, use the dictionary
        # for the answer. It is possible to specify some
        # useful properties as the part of the answer
        # (e.g. "cache")
        # answer by _get_page() always overrides all default properties
        #
        answer = self._get_page(topic, request_options=request_options)
        if not isinstance(answer, dict):
            answer = {"answer": answer}

        answer_dict = {
            'topic': topic,
            'topic_type': self._adapter_name,
            'format': self._get_output_format(topic),
            'cache': self._cache_needed,
            }
        answer_dict.update(answer)

        # pylint: disable=assignment-from-none
        filetype = self._get_filetype(topic)
        if filetype:
            answer_dict["filetype"] = filetype
        return answer_dict

    @classmethod
    def local_repository_location(cls, cheat_sheets_location=False):
        """
        Return local repository location.
        If name `self._repository_url` for the class is not specified, return None
        It is possible that several adapters has the same repository_url,
        in this case they should use the same local directory.
        If for some reason the local repository location should be overridden
        (e.g. if several different branches of the same repository are used)
        if should set in `self._local_repository_location` of the adapter.
        If `cheat_sheets_location` is specified, return path of the cheat sheets
        directory instead of the repository directory.
        """

        dirname = None

        if cls._local_repository_location:
            dirname = cls._local_repository_location

        if not dirname and cls._repository_url:
            dirname = cls._repository_url
            if dirname.startswith('https://'):
                dirname = dirname[8:]
            elif dirname.startswith('http://'):
                dirname = dirname[7:]

        # if we did not manage to find out dirname up to this point,
        # that means that neither repository url, not repository location
        # is specified for the adapter, so it should be skipped
        if not dirname:
            return None

        if dirname.startswith('/'):
            return dirname

        # it is possible that several repositories will
        # be mapped to the same location name
        # (because only the last part of the path is used)
        # in this case provide the name in _local_repository_location
        # (detected by fetch.py)
        if '/' in dirname:
            dirname = dirname.split('/')[-1]

        path = os.path.join(CONFIG['path.repositories'], dirname)

        if cheat_sheets_location:
            path = os.path.join(path, cls._cheatsheet_files_prefix)

        return path

    @classmethod
    def repository_url(cls):
        """
        Return URL of the upstream repository
        """
        return cls._repository_url

    @classmethod
    def fetch_command(cls):
        """
        Initial fetch of the repository.
        Return cmdline that has to be executed to fetch the repository.
        Skipping if `self._repository_url` is not specified
        """
        if not cls._repository_url:
            return None

        # in this case `fetch` has to be implemented
        # in the distinct adapter subclass
        raise RuntimeError(
            "Do not known how to handle this repository: %s" % cls._repository_url)

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

        # in this case `update` has to be implemented
        # in the distinct adapter subclass
        raise RuntimeError(
            "Do not known how to handle this repository: %s" % cls._repository_url)

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

        # in this case `update` has to be implemented
        # in the distinct adapter subclass
        raise RuntimeError(
            "Do not known how to handle this repository: %s" % cls._repository_url)

    @classmethod
    def save_state(cls, state):
        """
        Save state `state` of the repository.
        Must be called after the cache clean up.
        """
        local_repository_dir = cls.local_repository_location()
        state_filename = os.path.join(local_repository_dir, '.cached_revision')
        open(state_filename, 'w').write(state)

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
        Return the command to get the list of updates
        since the last update whose id is saved as the repository state (`cached_state`).
        The list is used to invalidate the cache.
        """
        return None

    @classmethod
    def get_updates_list(cls, updated_files_list):
        """
        Return the pages that have to be invalidated if the files `updates_files_list`
        were updated in the repository.
        """
        if not cls._cheatsheet_files_prefix:
            return updated_files_list

        answer = []
        cut_len = len(cls._cheatsheet_files_prefix)
        for entry in updated_files_list:
            if entry.startswith(cls._cheatsheet_files_prefix):
                answer.append(entry[cut_len:])
            else:
                answer.append(entry)
        return answer

def all_adapters(as_dict=False):
    """
    Return list of all known adapters
    If `as_dict` is True, return dict {'name': adapter} instead of a list.
    """
    def _all_subclasses(cls):
        return set(cls.__subclasses__()).union(set(
            [s for c in cls.__subclasses__() for s in _all_subclasses(c)]
        ))

    if as_dict:
        return {x.name():x for x in _all_subclasses(Adapter)}
    return list(_all_subclasses(Adapter))

def adapter_by_name(name):
    """
    Return adapter having this name,
    or None if nothing found
    """
    return all_adapters(as_dict=True).get(name)
