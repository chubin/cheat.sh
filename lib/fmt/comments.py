"""
Extract text from the text-code stream and comment it.

Supports three modes of normalization and commenting:

    1. Don't add any comments
    2. Add comments
    3. Remove text, leave code only

Since several operations are quite expensive,
it actively uses caching.

Exported functions:

    beautify(text, lang, options)
    code_blocks(text)

Configuration parameters:
"""

from __future__ import print_function

import sys
import os
import textwrap
import hashlib
import re
from itertools import groupby, chain
from subprocess import Popen
from tempfile import NamedTemporaryFile

from config import CONFIG
from languages_data import VIM_NAME
import cache

FNULL = open(os.devnull, 'w')
TEXT = 0
CODE = 1
UNDEFINED = -1
CODE_WHITESPACE = -2
def _language_name(name):
    return VIM_NAME.get(name, name)


def _remove_empty_lines_from_beginning(lines):
    start = 0
    while start < len(lines) and lines[start].strip() == '':
        start += 1
    lines = lines[start:]
    return lines

def _remove_empty_lines_from_end(lines):
    end = len(lines) - 1
    while end >= 0 and lines[end].strip() == '':
        end -= 1
    lines = lines[:end+1]
    return lines

def _cleanup_lines(lines):
    """
    Cleanup `lines` a little bit: remove empty lines at the beginning
    and at the end; remove too many empty lines in between.
    """
    lines = _remove_empty_lines_from_beginning(lines)
    lines = _remove_empty_lines_from_end(lines)
    if lines == []:
        return lines
    # remove repeating empty lines
    lines = list(chain.from_iterable(
        [(list(x[1]) if x[0] else [''])
         for x in groupby(lines, key=lambda x: x.strip() != '')]))

    return lines


def _line_type(line):
    """
    Classify each line and say which of them
    are text (0) and which of them are code (1).

    A line is considered to be code,
    if it starts with four spaces.

    A line is considerer to be text if it is not
    empty and is not code.

    If line is empty, it is considered to be
    code if it surrounded but two other code lines,
    or if it is the first/last line and it has
    code on the other side.
    """
    if line.strip() == '':
        return UNDEFINED

    # some line may start with spaces but still be not code.
    # we need some heuristics here, but for the moment just
    # whitelist such cases:
    if line.strip().startswith('* ') or re.match(r'[0-9]+\.', line.strip()):
        return TEXT

    if line.startswith('   '):
        return CODE
    return TEXT

def _classify_lines(lines):
    line_types = [_line_type(line) for line in lines]

    # pass 2:
    # adding empty code lines to the code
    for i in range(len(line_types) - 1):
        if line_types[i] == CODE and line_types[i+1] == UNDEFINED:
            line_types[i+1] = CODE_WHITESPACE
            changed = True

    for i in range(len(line_types) - 1)[::-1]:
        if line_types[i] == UNDEFINED and line_types[i+1] == CODE:
            line_types[i] = CODE_WHITESPACE
            changed = True
    line_types = [CODE if x == CODE_WHITESPACE else x for x in line_types]

    # pass 3:
    # fixing undefined line types (-1)
    changed = True
    while changed:
        changed = False

        # changing all lines types that are near the text

        for i in range(len(line_types) - 1):
            if line_types[i] == TEXT and line_types[i+1] == UNDEFINED:
                line_types[i+1] = TEXT
                changed = True

        for i in range(len(line_types) - 1)[::-1]:
            if line_types[i] == UNDEFINED and line_types[i+1] == TEXT:
                line_types[i] = TEXT
                changed = True

    # everything what is still undefined, change to code type
    line_types = [CODE if x == UNDEFINED else x for x in line_types]
    return line_types

def _unindent_code(line, shift=0):
    if shift == -1 and line != '':
        return ' ' + line

    if shift > 0 and line.startswith(' '*shift):
        return line[shift:]

    return line

def _wrap_lines(lines_classes, unindent_code=False):
    """
    Wrap classified lines. Add the split lines to the stream.
    If `unindent_code` is True, remove leading four spaces.
    """

    result = []
    for line_type, line_content in lines_classes:
        if line_type == CODE:

            shift = 3 if unindent_code else -1
            result.append((line_type, _unindent_code(line_content, shift=shift)))
        else:
            if line_content.strip() == "":
                result.append((line_type, ""))
            for line in textwrap.fill(line_content).splitlines():
                result.append((line_type, line))

    return result

def _run_vim_script(script_lines, text_lines):
    """
    Apply `script_lines` to `lines_classes`
    and returns the result
    """

    script_vim = NamedTemporaryFile(delete=True)
    textfile = NamedTemporaryFile(delete=True)

    open(script_vim.name, "w").write("\n".join(script_lines))
    open(textfile.name, "w").write("\n".join(text_lines))

    script_vim.file.close()
    textfile.file.close()

    my_env = os.environ.copy()
    my_env['HOME'] = CONFIG["path.internal.vim"]

    cmd = ["script", "-q", "-c",
           "vim -S %s %s" % (script_vim.name, textfile.name)]

    Popen(cmd, shell=False,
          stdin=open(os.devnull, 'r'),
          stdout=FNULL, stderr=FNULL, env=my_env).communicate()

    return open(textfile.name, "r").read()

def _commenting_script(lines_blocks, filetype):
    script_lines = []
    block_start = 1
    for block in lines_blocks:
        lines = list(block[1])

        block_end = block_start + len(lines)-1

        if block[0] == 0:
            comment_type = 'sexy'
            if block_end - block_start < 1 or filetype == 'ruby':
                comment_type = 'comment'

            script_lines.insert(0, "%s,%s call NERDComment(1, '%s')"
                                % (block_start, block_end, comment_type))
            script_lines.insert(0, "%s,%s call NERDComment(1, 'uncomment')"
                                % (block_start, block_end))

        block_start = block_end + 1

    script_lines.insert(0, "set ft=%s" % _language_name(filetype))
    script_lines.append("wq")

    return script_lines

def _beautify(text, filetype, add_comments=False, remove_text=False):
    """
    Main function that actually does the whole beautification job.
    """

    # We shift the code if and only if we either convert the text into comments
    # or remove the text completely. Otherwise the code has to remain aligned
    unindent_code = add_comments or remove_text

    lines = [x.decode("utf-8").rstrip('\n') for x in text.splitlines()]
    lines = _cleanup_lines(lines)
    lines_classes = zip(_classify_lines(lines), lines)
    lines_classes = _wrap_lines(lines_classes, unindent_code=unindent_code)

    if remove_text:
        lines = [line[1] for line in lines_classes if line[0] == 1]
        lines = _cleanup_lines(lines)
        output = "\n".join(lines)
        if not output.endswith('\n'):
            output += "\n"
    elif not add_comments:
        output = "\n".join(line[1] for line in lines_classes)
    else:
        lines_blocks = groupby(lines_classes, key=lambda x: x[0])
        script_lines = _commenting_script(lines_blocks, filetype)
        output = _run_vim_script(
            script_lines,
            [line for (_, line) in lines_classes])

    return output

def code_blocks(text, wrap_lines=False, unindent_code=False):
    """
    Split `text` into blocks of text and code.
    Return list of tuples TYPE, TEXT
    """
    text = text.encode('utf-8')

    lines = [x.rstrip('\n') for x in text.splitlines()]
    lines_classes = zip(_classify_lines(lines), lines)

    if wrap_lines:
        lines_classes = _wrap_lines(lines_classes, unindent_code=unindent_code)

    lines_blocks = groupby(lines_classes, key=lambda x: x[0])
    answer = [(x[0], "\n".join([y[1] for y in x[1]])+"\n") for x in lines_blocks]
    return answer


def beautify(text, lang, options):
    """
    Process input `text` according to the specified `mode`.
    Adds comments if needed, according to the `lang` rules.
    Caches the results.
    The whole work (except caching) is done by _beautify().
    """

    options = options or {}
    beauty_options = dict((k, v) for k, v in options.items() if k in
                          ['add_comments', 'remove_text'])

    mode = ''
    if beauty_options.get('add_comments'):
        mode += 'c'
    if beauty_options.get('remove_text'):
        mode += 'q'

    if beauty_options == {}:
        # if mode is unknown, just don't transform the text at all
        return text

    if isinstance(text, str):
        text = text.encode('utf-8')
    digest = "t:%s:%s:%s" % (hashlib.md5(text).hexdigest(), lang, mode)

    # temporary added line that removes invalid cache entries
    # that used wrong commenting methods
    if lang in ["git", "django", "flask", "cmake"]:
        cache.delete(digest)

    answer = cache.get(digest)
    if answer:
        return answer
    answer = _beautify(text, lang, **beauty_options)
    cache.put(digest, answer)

    return answer

def __main__():
    text = sys.stdin.read()
    filetype = sys.argv[1]
    options = {
        "": {},
        "c": dict(add_comments=True),
        "C": dict(add_comments=False),
        "q": dict(remove_text=True),
    }[sys.argv[2]]
    result = beautify(text, filetype, options)
    sys.stdout.write(result)

if __name__ == '__main__':
    __main__()
