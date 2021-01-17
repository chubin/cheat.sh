"""

Programming languages information.
Will be (probably) moved to a separate file/directory
from the project tree.

"""

import pygments.lexers

LEXER = {
    "assembly"  : pygments.lexers.NasmLexer,
    "awk"       : pygments.lexers.AwkLexer,
    "bash"      : pygments.lexers.BashLexer,
    "basic"     : pygments.lexers.QBasicLexer,
    "bf"        : pygments.lexers.BrainfuckLexer,
    "chapel"    : pygments.lexers.ChapelLexer,
    "clojure"   : pygments.lexers.ClojureLexer,
    "coffee"    : pygments.lexers.CoffeeScriptLexer,
    "cpp"       : pygments.lexers.CppLexer,
    "c"         : pygments.lexers.CLexer,
    "csharp"    : pygments.lexers.CSharpLexer,
    "d"         : pygments.lexers.DLexer,
    "dart"      : pygments.lexers.DartLexer,
    "delphi"    : pygments.lexers.DelphiLexer,
    "elisp"     : pygments.lexers.EmacsLispLexer,
    "elixir"    : pygments.lexers.ElixirLexer,
    "elm"       : pygments.lexers.ElmLexer,
    "erlang"    : pygments.lexers.ErlangLexer,
    "factor"    : pygments.lexers.FactorLexer,
    "forth"     : pygments.lexers.ForthLexer,
    "fortran"   : pygments.lexers.FortranLexer,
    "fsharp"    : pygments.lexers.FSharpLexer,
    "git"       : pygments.lexers.BashLexer,
    "go"        : pygments.lexers.GoLexer,
    "groovy"    : pygments.lexers.GroovyLexer,
    "haskell"   : pygments.lexers.HaskellLexer,
    "java"      : pygments.lexers.JavaLexer,
    "js"        : pygments.lexers.JavascriptLexer,
    "julia"     : pygments.lexers.JuliaLexer,
    "kotlin"    : pygments.lexers.KotlinLexer,
    "latex"     : pygments.lexers.TexLexer,
    "lisp"      : pygments.lexers.CommonLispLexer,
    "lua"       : pygments.lexers.LuaLexer,
    "mathematica": pygments.lexers.MathematicaLexer,
    "matlab"    : pygments.lexers.MatlabLexer,
    "mongo" :   pygments.lexers.JavascriptLexer,
    "nim"       : pygments.lexers.NimrodLexer,
    "objective-c": pygments.lexers.ObjectiveCppLexer,
    "ocaml"     : pygments.lexers.OcamlLexer,
    "octave"    : pygments.lexers.OctaveLexer,
    "perl"      : pygments.lexers.PerlLexer,
    "perl6"     : pygments.lexers.Perl6Lexer,
    "php"       : pygments.lexers.PhpLexer,
    "psql"  :   pygments.lexers.PostgresLexer,
    "python"    : pygments.lexers.PythonLexer,
    "python3"   : pygments.lexers.Python3Lexer,
    "r"         : pygments.lexers.SLexer,
    "racket"    : pygments.lexers.RacketLexer,
    "ruby"      : pygments.lexers.RubyLexer,
    "rust"      : pygments.lexers.RustLexer,
    "solidity"  : pygments.lexers.JavascriptLexer,
    "scala"     : pygments.lexers.ScalaLexer,
    "scheme":   pygments.lexers.SchemeLexer,
    "psql"   :   pygments.lexers.SqlLexer,
    "sql"   :   pygments.lexers.SqlLexer,
    "swift"     : pygments.lexers.SwiftLexer,
    "tcl"       : pygments.lexers.TclLexer,
    "tcsh"      : pygments.lexers.TcshLexer,
    "vb"        : pygments.lexers.VbNetLexer,
    "vbnet" :   pygments.lexers.VbNetLexer,
    "vim"       : pygments.lexers.VimLexer,

    # experimental
    "arduino":  pygments.lexers.ArduinoLexer,
    "pike"  :   pygments.lexers.PikeLexer,
    "eiffel" :  pygments.lexers.EiffelLexer,
    "clean"  :  pygments.lexers.CleanLexer,
    "dylan" :   pygments.lexers.DylanLexer,

# not languages
    "cmake"     : pygments.lexers.CMakeLexer,
    "django"    : pygments.lexers.PythonLexer,
    "flask"     : pygments.lexers.PythonLexer,
}

# canonical names are on the right side
LANGUAGE_ALIAS = {
    'asm'       :   'assembly',
    'assembler' :   'assembly',
    'c++'       :   'cpp',
    'c#'        :   'csharp',
    'clisp'     :   'lisp',
    'coffeescript': 'coffee',
    'cplusplus' :   'cpp',
    'dlang'     :   'd',
    'f#'        :   'fsharp',
    'golang'    :   'go',
    'javascript':   'js',
    'objc'      :   'objective-c',
    'p6'        :   'perl6',
    'sh'        :   'bash',
    'visualbasic':  'vb',
    'vba'       :   'vb',
    'wolfram'   :   'mathematica',
    'mma'       :   'mathematica',
    'wolfram-mathematica': 'mathematica',
    'm'         :   'octave',
}

VIM_NAME = {
    'assembly'  :   'asm',
    'bash'      :   'sh',
    'coffeescript': 'coffee',
    'csharp'    :   'cs',
    'delphi'    :   'pascal',
    'dlang'     :   'd',
    'elisp'     :   'newlisp',
    'latex'     :   'tex',
    'forth'     :   'fs',
    'nim'       :   'nimrod',
    'perl6'     :   'perl',
    'python3'   :   'python',
    'python-3.x':   'python',
    'tcsh'      :   'sh',
    'solidity'  :   'js',
    'mathematica':  'mma',
    'wolfram-mathematica': 'mma',
    'psql'      :   'sql',

    # not languages
    'cmake'     :   'sh',
    'git'       :   'sh',
    'django'    :   'python',
    'flask'     :   'python',
}

SO_NAME = {
    'coffee'    :   'coffeescript',
    'js'        :   'javascript',
    'python3'   :   'python-3.x',
    'vb'        :   'vba',
    'mathematica':  'wolfram-mathematica',
}


#
# conversion of internal programmin language names
# into canonical cheat.sh names
#

ATOM_FT_NAME = {
}

EMACS_FT_NAME = {
    "asm-mode"             : "asm",
    "awk-mode"             : "awk",
    "sh-mode"              : "bash",
    # basic
    "brainfuck-mode"       : "bf",
    # chapel
    "clojure-mode"         : "clojure",
    "coffee-mode"          : "coffee",
    "c++-mode"             : "cpp",
    "c-mode"               : "c",
    "csharp-mode"          : "csharp",
    "d-mode"               : "d",
    "dart-mode"            : "dart",
    "dylan-mode"           : "dylan",
    "delphi-mode"          : "delphi",
    "emacs-lisp-mode"      : "elisp",
    # elixir
    "elm-mode"             : "elm",
    "erlang-mode"          : "erlang",
    # factor
    "forth-mode"           : "forth",
    "fortran-mode"         : "fortran",
    "fsharp-mode"          : "fsharp",
    "go-mode"              : "go",
    "groovy-mode"          : "groovy",
    "haskell-mode"         : "haskell",
    # "hy-mode"
    "java-mode"            : "java",
    "js-jsx-mode"          : "js",
    "js-mode"              : "js",
    "js2-jsx-mode"         : "js",
    "js2-mode"             : "js",
    "julia-mode"           : "julia",
    "kotlin-mode"          : "kotlin",
    "lisp-interaction-mode": "lisp",
    "lisp-mode"            : "lisp",
    "lua-mode"             : "lua",
    # mathematica
    "matlab-mode"          : "matlab",
    # mongo
    "objc-mode"            : "objective-c",
    # ocaml
    "perl-mode"            : "perl",
    "perl6-mode"           : "perl6",
    "php-mode"             : "php",
    # psql
    "python-mode"          : "python",
    # python3
    # r -- ess looks it, but I don't know the mode name off hand
    "racket-mode"          : "racket",
    "ruby-mode"            : "ruby",
    "rust-mode"            : "rust",
    "solidity-mode"        : "solidity",
    "scala-mode"           : "scala",
    "scheme-mode"          : "scheme",
    "sql-mode"             : "sql",
    "swift-mode"           : "swift",
    "tcl-mode"             : "tcl",
    # tcsh
    "visual-basic-mode"    : "vb",
    # vbnet
    # vim
}

SUBLIME_FT_NAME = {
}

VIM_FT_NAME = {
    'asm':          'assembler',
    'javascript':   'js',
    'octave':       'matlab',
}

VSCODE_FT_NAME = {
}

def rewrite_editor_section_name(section_name):
    """
    section name cen be specified in form "editor:editor-filetype"
    and it will be rewritten into form "filetype"
    basing on the editor filetypes names data.
    If editor name is unknown, it is just cut off:  notepad:js => js

    Known editors:
        * atom
        * vim
        * emacs
        * sublime
        * vscode

    >>> rewrite_editor_section_name('js')
    'js'
    >>> rewrite_editor_section_name('vscode:js')
    'js'
    """
    if ':' not in section_name:
        return section_name

    editor_name, section_name = section_name.split(':', 1)
    editor_name_mapping = {
        'atom':     ATOM_FT_NAME,
        'emacs':    EMACS_FT_NAME,
        'sublime':  SUBLIME_FT_NAME,
        'vim':      VIM_FT_NAME,
        'vscode':   VSCODE_FT_NAME,
    }
    if editor_name not in editor_name_mapping:
        return section_name
    return editor_name_mapping[editor_name].get(section_name, section_name)

def get_lexer_name(section_name):
    """
    Rewrite `section_name` for the further lexer search (for syntax highlighting)
    """
    if ':' in section_name:
        section_name = rewrite_editor_section_name(section_name)
    return LANGUAGE_ALIAS.get(section_name, section_name)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
