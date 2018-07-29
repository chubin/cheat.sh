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
    "go"        : pygments.lexers.GoLexer,
    "groovy"    : pygments.lexers.GroovyLexer,
    "haskell"   : pygments.lexers.HaskellLexer,
    "java"      : pygments.lexers.JavaLexer,
    "js"        : pygments.lexers.JavascriptLexer,
    "julia"     : pygments.lexers.JuliaLexer,
    "kotlin"    : pygments.lexers.KotlinLexer,
    "lisp"      : pygments.lexers.CommonLispLexer,
    "lua"       : pygments.lexers.LuaLexer,
    "mathematica": pygments.lexers.MathematicaLexer,
    "matlab"    : pygments.lexers.MatlabLexer,
    "mongo" :   pygments.lexers.JavascriptLexer,
    "objective-c": pygments.lexers.ObjectiveCppLexer,
    "ocaml"     : pygments.lexers.OcamlLexer,
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
}

VIM_NAME = {
    'assembly'  :   'asm',
    'bash'      :   'sh',
    'coffeescript': 'coffee',
    'csharp'    :   'cs',
    'delphi'    :   'pascal',
    'dlang'     :   'd',
    'elisp'     :   'newlisp',
    'forth'     :   'fs',
    'perl6'     :   'perl',
    'python3'   :   'python',
    'python-3.x':   'python',
    'tcsh'      :   'sh',
    'solidity'  :   'js',
    'mathematica':  'mma',
    'wolfram-mathematica': 'mma',
}

SO_NAME = {
    'coffee'    :   'coffeescript',
    'js'        :   'javascript',
    'python3'   :   'python-3.x',
    'vb'        :   'vba',
    'mathematica':  'wolfram-mathematica',
}
