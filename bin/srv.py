#!/usr/bin/env python
#
# Serving cheat.sh with `gevent`
#

from gevent.monkey import patch_all
from gevent.pywsgi import WSGIServer
patch_all()

import os
import sys

from app import app, CONFIG


if '--debug' in sys.argv:
    # Not all debug mode features are available under `gevent`
    # https://github.com/pallets/flask/issues/3825
    app.debug = True

if 'CHEATSH_PORT' in os.environ:
    port = int(os.environ.get('CHEATSH_PORT'))
else:
    port = CONFIG['server.port']

srv = WSGIServer((CONFIG['server.bind'], port), app)
print("Starting gevent server on {}:{}".format(srv.address[0], srv.address[1]))
srv.serve_forever()
