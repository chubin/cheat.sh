FROM alpine:latest
# fetching cheat sheets
## installing dependencies
RUN apk add --update --no-cache git py3-six py3-pygments py3-yaml py3-gevent \
      libstdc++ py3-colorama py3-requests py3-icu py3-redis
## building missing python packages
RUN apk add --no-cache --virtual build-deps py3-pip g++ python3-dev \
    && pip3 install --no-cache-dir rapidfuzz colored polyglot pycld2 \
    && apk del build-deps
## copying
WORKDIR /app
COPY . /app
RUN mkdir -p /root/.cheat.sh/log/ \
    && python3 lib/fetch.py fetch-all

# installing server dependencies
#RUN apk add --update --no-cache py3-cffi py2-pip py2-gevent \
#    py2-flask py2-requests py2-pygments py2-redis \
#    py2-cffi py2-icu bash vim gawk sed \
#    && apk add --no-cache --virtual build-deps python3-dev build-base \
#    && pip3 install -r requirements.txt \
#    && apk del build-deps
ENTRYPOINT ["python3"]
CMD ["bin/srv.py"]
