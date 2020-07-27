FROM alpine:3.10
WORKDIR /app
COPY requirements.txt /app/
RUN apk add --update --no-cache python2 py2-pip py2-gevent \
    py2-flask py2-requests py2-pygments py2-redis \
    py2-cffi py2-icu bash vim gawk sed \
    && apk add --no-cache --virtual build-deps python2-dev \
    build-base git \
    && pip install -r requirements.txt \
    && apk del build-deps
COPY . /app
RUN apk add --update --no-cache curl git py2-virtualenv \
    && ./share/cht.sh.txt --standalone-install
ENTRYPOINT ["python2"]
CMD ["bin/srv.py"]
