"""
Adapter for https://github.com/cheat/cheat

Cheatsheets are located in `cheat/cheatsheets/`
Each cheat sheet is a separate file without extension
"""

# pylint: disable=relative-import,abstract-method

from .git_adapter import GitRepositoryAdapter

class Cheat(GitRepositoryAdapter):
    """
    cheat/cheat adapter
    """

    _adapter_name = "cheat"
    _output_format = "code"
    _cache_needed = True
    _repository_url = "https://github.com/cheat/cheatsheets"
    _cheatsheet_files_prefix = ""
    _cheatsheet_file_mask = "*"
