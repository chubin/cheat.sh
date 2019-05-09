"""
Parse query arguments.
"""

def parse_args(args):
    """
    Parse arguments and options.
    Replace short options with their long counterparts.
    """
    result = {
        'add_comments':  True,
    }

    query = ""
    newargs = {}
    for key, val in args.items():
        if val == "" or val == [] or val == ['']:
            query += key
            continue
        if val == 'True':
            val = True
        if val == 'False':
            val = False
        newargs[key] = val

    options_meaning = {
        "c": dict(add_comments=False, unindent_code=False),
        "C": dict(add_comments=False, unindent_code=True),
        "Q": dict(remove_text=True),
        'q': dict(quiet=True),
        'T': {'no-terminal': True},
    }
    for option, meaning in options_meaning.items():
        if option in query:
            result.update(meaning)

    result.update(newargs)

    return result
