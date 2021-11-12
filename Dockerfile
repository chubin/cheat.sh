FROM alpine:3.14
# fetching cheat sheets
## installing dependencies
RUN apk add --update --no-cache git py3-six py3-pygments py3-yaml py3-gevent \
      libstdc++ py3-colorama py3-requests py3-icu py3-redis sed
## copying
WORKDIR /app
COPY . /app
## building missing python packages
RUN apk add --no-cache --virtual build-deps py3-pip g++ python3-dev libffi-dev \
    && pip3 install --no-cache-dir --upgrade pygments \
    && pip3 install --no-cache-dir -r requirements.txt \
    && apk del build-deps
# fetching dependencies
RUN mkdir -p /root/.cheat.sh/log/ \
    && python3 lib/fetch.py fetch-all

# installing server dependencies
RUN apk add --update --no-cache py3-jinja2 py3-flask bash gawk
ENTRYPOINT ["python3", "-u", "bin/srv.py"]
CMD [""]
