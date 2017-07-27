#!/usr/bin/python

import os
import re

class LearnXYAdapter(object):
    _learn_xy_path = "/home/igor/git/github.com/adambard/learnxinyminutes-docs"

    def __init__(self):

        self._whole_cheatsheet = self._read_cheatsheet()
        self._blocks = self._extract_blocks()
        self._topics_list = [x for x,y in self._blocks] + [":learn"]

    def _read_cheatsheet(self):
        filename = os.path.join(self._learn_xy_path, self._filename)

        with open(filename) as f:
            code_mode = False
            answer = []
            for line in f.readlines():
                if line.startswith('```'):
                    if not code_mode:
                        code_mode = True
                        continue
                    else:
                        code_mode = False
                if code_mode:
                    answer.append(line.rstrip('\n'))
            return answer

    def _extract_blocks(self):
        lines = self._whole_cheatsheet
        answer = []

        block = []
        block_name = "Start"
        for before, now, after in zip([""]+lines, lines, lines[1:]):
            new_block_name = self._is_block_separator(before, now, after)
            if new_block_name:
                print new_block_name
                if block_name:
                    answer.append((block_name, self._cut_block(block)))
                block_name = new_block_name
                block = []
                continue
            else:
                block.append(before)

        answer.append((block_name, self._cut_block(block)))
        return answer

    def is_valid(self, name):
        for x in self._topics_list:
            if x == name:
                return True
        return False

    def get_list(self, prefix=False):
        if prefix:
            return ["%s/%s" % (self._prefix, x) for x in self._topics_list]
        else:
            return self._topics_list

    def get_cheat_sheet(self, name, partial=False):
        if name == ":list":
            return "\n".join(self.get_list()) + "\n"

        if name == ":learn":
            return "\n".join(self._whole_cheatsheet) + "\n"

        if partial:
            possible_names = []
            for x, y in self._blocks:
                if x.startswith(name):
                    possible_names.append(x)
            if len(possible_names) == 0 or len(possible_names) > 1:
                return None
            name = possible_names[0]

        for x, y in self._blocks:
            if x == name:
                return "\n".join(y)

        return None

#
# Various cheat sheets
#

class LearnClojureAdapter(LearnXYAdapter):
    _prefix = "clojure"
    _filename = "clojure.html.markdown"

    def _is_block_separator(self, before, now, after):
        if (    re.match(r'\s*$', before) 
            and re.match(r';\s*', now)
            and re.match(r';;;;;;+', after)):
            block_name = re.sub(';\s*', '', now)
            block_name = '_'.join([x.strip(",&:") for x in  block_name.strip(", ").split()])
            # replace_with = {
            #     'More_about_Objects': 
            #         'Prototypes',
            # }
            # for k in replace_with:
            #     if k in block_name:
            #         block_name = replace_with[k]
            return block_name
        else:
            return None

    @staticmethod
    def _cut_block(block):
        answer = block[2:]
        if answer[0].split() == '':
            answer = answer[1:]
        if answer[-1].split() == '':
            answer = answer[:1]
        return answer

class LearnCppAdapter(LearnXYAdapter):
    _prefix = "c++"
    _filename = "c++.html.markdown"

    def _is_block_separator(self, before, now, after):
        if (    re.match(r'////////*', before) 
            and re.match(r'// ', now)
            and re.match(r'////////*', after)):
            block_name = re.sub('//\s*', '', now).replace('(', '').replace(')', '')
            block_name = '_'.join(block_name.strip(", ").split())
            replace_with = {
                'More_about_Objects': 
                    'Prototypes',
            }
            for k in replace_with:
                if k in block_name:
                    block_name = replace_with[k]
            return block_name
        else:
            return None

    @staticmethod
    def _cut_block(block):
        answer = block[2:-1]
        if answer == []:
            return answer
        if answer[0].split() == '':
            answer = answer[1:]
        if answer[-1].split() == '':
            answer = answer[:1]
        return answer

class LearnElixirAdapter(LearnXYAdapter):
    _prefix = "elixir"
    _filename = "elixir.html.markdown"

    def _is_block_separator(self, before, now, after):
        if (    re.match(r'## ---*', before) 
            and re.match(r'## --', now)
            and re.match(r'## ---*', after)):
            block_name = re.sub('## --\s*', '', now)
            block_name = '_'.join(block_name.strip(", ").split())
            replace_with = {
                'More_about_Objects': 
                    'Prototypes',
            }
            for k in replace_with:
                if k in block_name:
                    block_name = replace_with[k]
            return block_name
        else:
            return None

    @staticmethod
    def _cut_block(block):
        answer = block[2:-1]
        if answer[0].split() == '':
            answer = answer[1:]
        if answer[-1].split() == '':
            answer = answer[:1]
        return answer


class LearnElmAdapter(LearnXYAdapter):
    _prefix = "elm"
    _filename = "elm.html.markdown"

    def _is_block_separator(self, before, now, after):
        if (    re.match('\s*', before) 
            and re.match(r'\{--.*--\}', now)
            and re.match('\s*', after)):
            block_name = re.sub('\{--+\s*', '', now)
            block_name = re.sub('--\}', '', block_name)
            block_name = '_'.join(block_name.strip(", ").split())
            replace_with = {
                'More_about_Objects': 
                    'Prototypes',
            }
            for k in replace_with:
                if k in block_name:
                    block_name = replace_with[k]
            return block_name
        else:
            return None

    @staticmethod
    def _cut_block(block):
        answer = block[2:-1]
        if answer[0].split() == '':
            answer = answer[1:]
        if answer[-1].split() == '':
            answer = answer[:1]
        return answer

class LearnErlangAdapter(LearnXYAdapter):
    _prefix = "erlang"
    _filename = "erlang.html.markdown"

    def _is_block_separator(self, before, now, after):
        if (re.match('%%%%%%+', before) 
            and re.match('%%\s+[0-9]+\.', now)
            and re.match('%%%%%%+', after)):
            block_name = re.sub('%%+\s+[0-9]+\.\s*', '', now)
            block_name = '_'.join(block_name.strip('.').strip().split())
            return block_name
        else:
            return None

    @staticmethod
    def _cut_block(block):
        answer = block[2:-1]
        if answer[0].split() == '':
            answer = answer[1:]
        if answer[-1].split() == '':
            answer = answer[:1]
        return answer

class LearnLuaAdapter(LearnXYAdapter):
    _prefix = "lua"
    _filename = "lua.html.markdown"

    def _is_block_separator(self, before, now, after):
        if (re.match('-----+', before) 
            and re.match('-------+', after)
            and re.match('--\s+[0-9]+\.', now)):
            block_name = re.sub('--+\s+[0-9]+\.\s*', '', now)
            block_name = '_'.join(block_name.strip('.').strip().split())
            replace_with = {
                '1_Metatables_and_metamethods': 
                    'Metatables',
                '2_Class-like_tables_and_inheritance':
                    'Class-like_tables',
                'Variables_and_flow_control':
                    'Flow_control',
            }
            if block_name in replace_with:
                block_name = replace_with[block_name]
            return block_name
        else:
            return None

    @staticmethod
    def _cut_block(block):
        answer = block[2:-1]
        if answer[0].split() == '':
            answer = answer[1:]
        if answer[-1].split() == '':
            answer = answer[:1]
        return answer

class LearnJavaScriptAdapter(LearnXYAdapter):
    _prefix = "js"
    _filename = "javascript.html.markdown"

    def _is_block_separator(self, before, now, after):
        if (    re.match('//////+', before) 
            and re.match('//+\s+[0-9]+\.', now)
            and re.match('\s*', after)):
            block_name = re.sub('//+\s+[0-9]+\.\s*', '', now)
            block_name = '_'.join(block_name.strip(", ").split())
            replace_with = {
                'More_about_Objects': 
                    'Prototypes',
            }
            for k in replace_with:
                if k in block_name:
                    block_name = replace_with[k]
            return block_name
        else:
            return None

    @staticmethod
    def _cut_block(block):
        answer = block[2:-1]
        if answer[0].split() == '':
            answer = answer[1:]
        if answer[-1].split() == '':
            answer = answer[:1]
        return answer

class LearnJuliaAdapter(LearnXYAdapter):
    _prefix = "julia"
    _filename = "julia.html.markdown"

    def _is_block_separator(self, before, now, after):
        if (    re.match('####+', before) 
            and re.match(r'##\s*', now)
            and re.match('####+', after)):
            block_name = re.sub(r'##\s+[0-9]+\.\s*', '', now)
            block_name = '_'.join(block_name.strip(", ").split())
            #replace_with = {
            #    'More_about_Objects': 
            #        'Prototypes',
            #}
            #for k in replace_with:
            #    if k in block_name:
            #        block_name = replace_with[k]
            return block_name
        else:
            return None

    @staticmethod
    def _cut_block(block):
        answer = block[2:-1]
        if answer[0].split() == '':
            answer = answer[1:]
        if answer[-1].split() == '':
            answer = answer[:1]
        return answer

class LearnHaskellAdapter(LearnXYAdapter):
    _prefix = "haskell"
    _filename = "haskell.html.markdown"

    def _is_block_separator(self, before, now, after):
        if (    re.match('------+', before) 
            and re.match('--+\s+[0-9]+\.', now)
            and re.match('------+', after)):
            block_name = re.sub('--+\s+[0-9]+\.\s*', '', now)
            block_name = '_'.join(block_name.strip(", ").split())
            replace_with = {
                'More_about_Objects': 
                    'Prototypes',
            }
            for k in replace_with:
                if k in block_name:
                    block_name = replace_with[k]
            return block_name
        else:
            return None

    @staticmethod
    def _cut_block(block):
        answer = block[2:-1]
        if answer[0].split() == '':
            answer = answer[1:]
        if answer[-1].split() == '':
            answer = answer[:1]
        return answer

class LearnKotlinAdapter(LearnXYAdapter):
    _prefix = "kotlin"
    _filename = "kotlin.html.markdown"

    def _is_block_separator(self, before, now, after):
        if (re.match('#######+', before) 
            and re.match('#######+', after)
            and re.match('#+\s+[0-9]+\.', now)):
            block_name = re.sub('#+\s+[0-9]+\.\s*', '', now)
            block_name = '_'.join(block_name.strip().split())
            return block_name
        else:
            return None

    @staticmethod
    def _cut_block(block):
        answer = block[2:-1]
        if answer[0].split() == '':
            answer = answer[1:]
        if answer[-1].split() == '':
            answer = answer[:1]
        return answer

class LearnOCamlAdapter(LearnXYAdapter):
    _prefix = "ocaml"
    _filename = "ocaml.html.markdown"

    def _is_block_separator(self, before, now, after):
        if (    re.match('\s*', before) 
            and re.match(r'\(\*\*\*+', now)
            and re.match('\s*', after)):
            block_name = re.sub(r'\(\*\*\*+\s*', '', now)
            block_name = re.sub(r'\s*\*\*\*\)', '', block_name)
            block_name = '_'.join(block_name.strip(", ").split())
            replace_with = {
                'More_about_Objects': 
                    'Prototypes',
            }
            for k in replace_with:
                if k in block_name:
                    block_name = replace_with[k]
            return block_name
        else:
            return None

    @staticmethod
    def _cut_block(block):
        answer = block[2:-1]
        if answer[0].split() == '':
            answer = answer[1:]
        if answer[-1].split() == '':
            answer = answer[:1]
        return answer

class LearnPerlAdapter(LearnXYAdapter):
    _prefix = "perl"
    _filename = "perl.html.markdown"

    def _is_block_separator(self, before, now, after):
        if re.match('####+\s+', now):
            block_name = re.sub('#+\s', '', now)
            block_name = '_'.join(block_name.strip().split())
            replace_with = {
                'Conditional_and_looping_constructs': 
                    'Control_Flow',
                'Perl_variable_types':
                    'Types',
                'Files_and_I/O':
                    'Files',
                'Writing_subroutines':
                    'Subroutines',
            }
            if block_name in replace_with:
                block_name = replace_with[block_name]
            return block_name
        else:
            return None

    @staticmethod
    def _cut_block(block):
        answer = block[2:]
        if len(answer) == 0:
            return answer
        if answer[0].split() == '':
            answer = answer[1:]
        if answer[-1].split() == '':
            answer = answer[:1]
        return answer

class LearnPHPAdapter(LearnXYAdapter):
    _prefix = "php"
    _filename = "php.html.markdown"

    def _is_block_separator(self, before, now, after):
        if (re.match(r'/\*\*\*\*\*+', before) 
            and re.match(r'\s*\*/', after)
            and re.match(r'\s*\*\s*', now)):
            block_name = re.sub(r'\s*\*\s*', '', now)
            block_name = re.sub(r'&', '', block_name)
            block_name = '_'.join(block_name.strip().split())
            return block_name
        else:
            return None

    @staticmethod
    def _cut_block(block):
        return block[2:]

class LearnPythonAdapter(LearnXYAdapter):
    _prefix = "python"
    _filename = "python.html.markdown"

    def _is_block_separator(self, before, now, after):
        if (re.match('#######+', before) 
            and re.match('#######+', after)
            and re.match('#+\s+[0-9]+\.', now)):
            block_name = re.sub('#+\s+[0-9]+\.\s*', '', now)
            block_name = '_'.join(block_name.strip().split())
            return block_name
        else:
            return None

    @staticmethod
    def _cut_block(block):
        answer = block[2:-1]
        if answer[0].split() == '':
            answer = answer[1:]
        if answer[-1].split() == '':
            answer = answer[:1]
        return answer

class LearnRubyAdapter(LearnXYAdapter):
    _prefix = "ruby"
    _filename = "ruby.html.markdown"

    def _is_block_separator(self, before, now, after):
        if (re.match('#######+', before) 
            and re.match('#######+', after)
            and re.match('#+\s+[0-9]+\.', now)):
            block_name = re.sub('#+\s+[0-9]+\.\s*', '', now)
            block_name = '_'.join(block_name.strip().split())
            return block_name
        else:
            return None

    @staticmethod
    def _cut_block(block):
        answer = block[2:-1]
        if answer[0].split() == '':
            answer = answer[1:]
        if answer[-1].split() == '':
            answer = answer[:1]
        return answer


#
# Exported functions
#

ADAPTERS = {
    'clojure'   : LearnClojureAdapter(),
    'c++'       : LearnCppAdapter(),
    'elixir'    : LearnElixirAdapter(),
    'elm'       : LearnElmAdapter(),
    'erlang'    : LearnErlangAdapter(),
    'haskell'   : LearnHaskellAdapter(),
    'js'        : LearnJavaScriptAdapter(),
    'julia'     : LearnJuliaAdapter(),
    'kotlin'    : LearnKotlinAdapter(),
    'lua'       : LearnLuaAdapter(),
    'ocaml'     : LearnOCamlAdapter(),
    'python'    : LearnPythonAdapter(),
    'php'       : LearnPHPAdapter(),
    'perl'      : LearnPerlAdapter(),
    'ruby'      : LearnRubyAdapter(),
}

def get_learnxiny(topic):
    lang, topic = topic.split('/', 1)
    if lang not in ADAPTERS:
        return ''
    return ADAPTERS[lang].get_cheat_sheet(topic)

def get_learnxiny_list():
    answer = []
    for k,v in ADAPTERS.items():
        answer += v.get_list(prefix=True)
    return answer

def is_valid_learnxy(topic):
    lang, topic = topic.split('/', 1)
    if lang not in ADAPTERS:
        return False

    return ADAPTERS[lang].is_valid(topic)

