FROM alpine:latest
WORKDIR /app
COPY . /app
RUN apk add --update --no-cache python2 py2-pip py2-gevent \
    py2-flask py2-requests py2-pygments py2-redis \
    py2-cffi py2-icu bash vim gawk sed \
    && apk add --no-cache --virtual build-deps python2-dev \
    build-base git \
    && pip install -r requirements.txt \
    && sh share/scripts/get-sheets.sh \
    && apk del build-deps
ENTRYPOINT ["python2"]
CMD ["bin/srv.py"]
