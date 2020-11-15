FROM python:3.9-slim

### copying app sources
WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

## fetching cheat sheets
RUN python3 lib/fetch.py fetch-all

ENTRYPOINT ["python3", "-u", "bin/srv.py"]
CMD [""]
