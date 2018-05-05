"""
Parse query arguments.
"""

def parse_args(args):
    """
    Parse arguments and options.
    Replace short options with their long counterparts.
    """
    result = {}

    query = ""
    for key, val in args.items():
        if val == "" or val == []:
            query += key
            continue

    if 'T' in query:
        result['no-terminal'] = True
    if 'q' in query:
        result['quiet'] = True

    options_meaning = {
        "c": dict(add_comments=True),
        "C": dict(add_comments=False),
        "Q": dict(remove_text=True),
    }
    for option, meaning in options_meaning.items():
        if option in query:
            result.update(meaning)

    for key, val in args.items():
        if val == 'True':
            val = True
        if val == 'False':
            val = False
        result[key] = val

    return result
