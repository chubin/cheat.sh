"""
POST requests processing.
Currently used only for new cheat sheets submission.

Configuration parameters:

    path.spool
"""

import string
import os
import random
from config import CONFIG

def _save_cheatsheet(topic_name, cheatsheet):
    """
    Save posted cheat sheet `cheatsheet` with `topic_name`
    in the spool directory
    """

    nonce = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(9))
    filename = topic_name.replace('/', '.') + "." + nonce
    filename = os.path.join(CONFIG["path.spool"], filename)

    open(filename, 'w').write(cheatsheet)

def process_post_request(req, topic):
    """
    Process POST request `req`.
    """
    for key, val in req.form.items():
        if key == '':
            if topic is None:
                topic_name = "UNNAMED"
            else:
                topic_name = topic
            cheatsheet = val
        else:
            if val == '':
                if topic is None:
                    topic_name = "UNNAMED"
                else:
                    topic_name = topic
                cheatsheet = key
            else:
                topic_name = key
                cheatsheet = val

        _save_cheatsheet(topic_name, cheatsheet)
