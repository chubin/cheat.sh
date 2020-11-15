FROM ubuntu:20.04

### copying app sources
WORKDIR /app
COPY . /app

RUN pip install --upgrade -r requirements.txt

## fetching cheat sheets
RUN python3 lib/fetch.py fetch-all

ENTRYPOINT ["python3", "-u", "bin/srv.py"]
CMD [""]
