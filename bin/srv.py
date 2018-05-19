#!/usr/bin/env python
# vim: set encoding=utf-8

"""
Main server program.
"""

from gevent.wsgi import WSGIServer
from gevent.monkey import patch_all
patch_all()

# pylint: disable=wrong-import-position,wrong-import-order
import sys
import logging
import os

import jinja2
from flask import Flask, request, send_from_directory, redirect

MYDIR = os.path.abspath(os.path.dirname(os.path.dirname('__file__')))
sys.path.append("%s/lib/" % MYDIR)

from globals import FILE_QUERIES_LOG, LOG_FILE, TEMPLATES, STATIC
from limits import Limits
from cheat_wrapper import cheat_wrapper
from post import process_post_request
from options import parse_args

from stateful_queries import save_query, last_query
# pylint: disable=wrong-import-position,wrong-import-order

if not os.path.exists(os.path.dirname(LOG_FILE)):
    os.makedirs(os.path.dirname(LOG_FILE))
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format='%(asctime)s %(message)s')

app = Flask(__name__) # pylint: disable=invalid-name
app.jinja_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader(TEMPLATES),
])

LIMITS = Limits()

def is_html_needed(user_agent):
    """
    Basing on `user_agent`, return whether it needs HTML or ANSI
    """
    plaintext_clients = ['curl', 'wget', 'fetch', 'httpie', 'lwp-request', 'python-requests']
    if any([x in user_agent for x in plaintext_clients]):
        return False
    return True

@app.route('/files/<path:path>')
def send_static(path):
    """
    Return static file `path`.
    Can be served by the HTTP frontend.
    """
    return send_from_directory(STATIC, path)

@app.route('/favicon.ico')
def send_favicon():
    """
    Return static file `favicon.ico`.
    Can be served by the HTTP frontend.
    """
    return send_from_directory(STATIC, 'favicon.ico')

@app.route('/malformed-response.html')
def send_malformed():
    """
    Return static file `malformed-response.html`.
    Can be served by the HTTP frontend.
    """
    return send_from_directory(STATIC, 'malformed-response.html')

def log_query(ip_addr, found, topic, user_agent):
    """
    Log processed query and some internal data
    """
    log_entry = "%s %s %s %s" % (ip_addr, found, topic, user_agent)
    with open(FILE_QUERIES_LOG, 'a') as my_file:
        my_file.write(log_entry.encode('utf-8')+"\n")

def get_request_ip(req):
    """
    Extract IP address from `request`
    """

    if req.headers.getlist("X-Forwarded-For"):
        ip_addr = req.headers.getlist("X-Forwarded-For")[0]
        if ip_addr.startswith('::ffff:'):
            ip_addr = ip_addr[7:]
    else:
        ip_addr = req.remote_addr
    if req.headers.getlist("X-Forwarded-For"):
        ip_addr = req.headers.getlist("X-Forwarded-For")[0]
        if ip_addr.startswith('::ffff:'):
            ip_addr = ip_addr[7:]
    else:
        ip_addr = req.remote_addr

    return ip_addr

@app.route("/", methods=['GET', 'POST'])
@app.route("/<path:topic>", methods=["GET", "POST"])
def answer(topic=None):
    """
    Main rendering function, it processes incoming weather queries.
    Depending on user agent it returns output in HTML or ANSI format.

    Incoming data:
        request.args
        request.headers
        request.remote_addr
        request.referrer
        request.query_string
    """

    user_agent = request.headers.get('User-Agent', '').lower()
    html_needed = is_html_needed(user_agent)
    options = parse_args(request.args)

    request_id = request.cookies.get('id')
    if topic is not None and topic.lstrip('/') == ':last':
        if request_id:
            topic = last_query(request_id)
        else:
            return "ERROR: you have to set id for your requests to use /:last\n"
    else:
        if request_id:
            save_query(request_id, topic)

    if request.method == 'POST':
        process_post_request(request, html_needed)
        if html_needed:
            return redirect("/")
        return "OK\n"

    if 'topic' in request.args:
        return redirect("/%s" % request.args.get('topic'))

    if topic is None:
        topic = ":firstpage"

    ip_address = get_request_ip(request)
    if '+' in topic:
        not_allowed = LIMITS.check_ip(ip_address)
        if not_allowed:
            return "429 %s\n" % not_allowed, 429

    result, found = cheat_wrapper(topic, request_options=options, html=is_html_needed(user_agent))

    log_query(ip_address, found, topic, user_agent)
    return result

SRV = WSGIServer(("", 8002), app) # log=None)
SRV.serve_forever()
