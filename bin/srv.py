#!/usr/bin/env python
# vim: set encoding=utf-8

import gevent
from gevent.wsgi import WSGIServer
from gevent.queue import Queue
from gevent.monkey import patch_all
from gevent.subprocess import Popen, PIPE, STDOUT
patch_all()

import sys
import logging
import os
import re
import requests
import socket
import subprocess
import time
import traceback
import dateutil.parser
import json

import jinja2
from flask import Flask, request, render_template, send_from_directory, send_file, make_response, redirect
app = Flask(__name__)

MYDIR = os.path.abspath(os.path.dirname( os.path.dirname('__file__') ))
sys.path.append("%s/lib/" % MYDIR)

from globals import LOG_FILE, TEMPLATES, STATIC, log, error

from cheat_wrapper import cheat_wrapper, save_cheatsheet

if not os.path.exists(os.path.dirname(LOG_FILE)):
    os.makedirs(os.path.dirname(LOG_FILE))
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format='%(asctime)s %(message)s')

my_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader(TEMPLATES),
])
app.jinja_loader = my_loader

def is_html_needed(user_agent):
    plaintext_clients = [ 'curl', 'wget', 'fetch', 'httpie', 'lwp-request', 'python-requests']
    if any([x in user_agent for x in plaintext_clients]):
        return False
    return True

@app.route('/files/<path:path>')
def send_static(path):
    return send_from_directory(STATIC, path)

@app.route('/favicon.ico')
def send_favicon():
    return send_from_directory(STATIC, 'favicon.ico')

@app.route('/malformed-response.html')
def send_malformed():
    return send_from_directory(STATIC, 'malformed-response.html')

@app.route("/", methods=['GET', 'POST'])
@app.route("/<path:topic>", methods=["GET", "POST"])
def answer(topic = None):
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

    if request.method == 'POST':
        for k, v in request.form.items():
            if k == '':
                if topic is None:
                    topic_name = "UNNAMED"
                else:
                    topic_name = topic
                cheatsheet = v
            else:
                if v == '':
                    if topic is None:
                        topic_name = "UNNAMED"
                    else:
                        topic_name = topic
                    cheatsheet = k
                else:
                    topic_name = k
                    cheatsheet = v

            save_cheatsheet(topic_name, cheatsheet)

        if html_needed:
            return redirect("/")
        else:
            return "OK\n"

    if 'topic' in request.args:
        return redirect("/%s" % request.args.get('topic'))

    if topic is None:
        topic = ":firstpage"

    answer = cheat_wrapper(topic, html=is_html_needed(user_agent))
    
    return answer

server = WSGIServer(("", 8002), app) # log=None)
server.serve_forever()

