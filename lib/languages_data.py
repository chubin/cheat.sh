"""

Programming languages information.
Will be (probably) moved to a separate file/directory
from the project tree.

"""

import pygments.lexers

LEXER = {
    "clojure":  pygments.lexers.ClojureLexer,
    "cpp"   :   pygments.lexers.CppLexer,
    "erlang":   pygments.lexers.ErlangLexer,
    "elixir":   pygments.lexers.ElixirLexer,
    "elm"   :   pygments.lexers.ElmLexer,
    "go"    :   pygments.lexers.GoLexer,
    "haskell":  pygments.lexers.HaskellLexer,
    "julia" :   pygments.lexers.JuliaLexer,
    "js"    :   pygments.lexers.JavascriptLexer,
    "kotlin":   pygments.lexers.KotlinLexer,
    "lua"   :   pygments.lexers.LuaLexer,
    "mongo" :   pygments.lexers.JavascriptLexer,
    "ocaml" :   pygments.lexers.OcamlLexer,
    "perl"  :   pygments.lexers.PerlLexer,
    "python":   pygments.lexers.PythonLexer,
    "php"   :   pygments.lexers.PhpLexer,
    "psql"  :   pygments.lexers.PostgresLexer,
    "ruby"  :   pygments.lexers.RubyLexer,
    "rust"  :   pygments.lexers.RustLexer,
    "scala" :   pygments.lexers.ScalaLexer,

    "c":        pygments.lexers.CLexer,

    "java":     pygments.lexers.JavaLexer,
    "groovy":   pygments.lexers.GroovyLexer,

    "sql":      pygments.lexers.SqlLexer,

    "r":        pygments.lexers.SLexer,

    "assembly": pygments.lexers.NasmLexer,

    "delphi":   pygments.lexers.DelphiLexer,

    "csharp":   pygments.lexers.CSharpLexer,
    "fsharp":   pygments.lexers.FSharpLexer,
    "vbnet" :   pygments.lexers.VbNetLexer,

    "perl6" :   pygments.lexers.Perl6Lexer,

    "objective-c": pygments.lexers.ObjectiveCppLexer,
    "swift" :   pygments.lexers.SwiftLexer,

    "scheme":   pygments.lexers.SchemeLexer,
    "racket":   pygments.lexers.RacketLexer,

    "awk":      pygments.lexers.AwkLexer,
    "bf":       pygments.lexers.BrainfuckLexer,
    "coffee":   pygments.lexers.CoffeeScriptLexer,
    "lisp":     pygments.lexers.CommonLispLexer,
    "elisp":    pygments.lexers.EmacsLispLexer,
    "factor":   pygments.lexers.FactorLexer,
    "forth":    pygments.lexers.ForthLexer,
    "fortran":  pygments.lexers.FortranLexer,
    "matlab":   pygments.lexers.MatlabLexer,
    "python3":  pygments.lexers.Python3Lexer,
    "bash":     pygments.lexers.BashLexer,
    "basic":    pygments.lexers.QBasicLexer,
    "tcsh":     pygments.lexers.TcshLexer,

    # experimental
    "arduino":  pygments.lexers.ArduinoLexer,
    "pike"  :   pygments.lexers.PikeLexer,
    "eiffel" :  pygments.lexers.EiffelLexer,
    "clean"  :  pygments.lexers.CleanLexer,
    "dlang"  :  pygments.lexers.DLexer,
    "dylan" :   pygments.lexers.DylanLexer,
    "chapel" :  pygments.lexers.ChapelLexer,
}

# canonical names are on the right side
LANGUAGE_ALIAS = {
    'coffeescript': 'coffee',
    'javascript':   'js',
    'clisp':        'lisp',
    'golang':       'go',
    'c++':          'cpp',
    'cplusplus':    'cpp',
    'c#':           'csharp',
    'f#':           'fsharp',
    'objc':         'objective-c',
    'sh':           'bash',
    'asm':          'assembly',
    'assembler':    'assembly',
}

VIM_NAME = {
    "assembly":     "asm",
    "dlang":        "d",
    "vbnet":        "vb",
    "delphi":       "pascal",
    "bash":         "sh",
}
