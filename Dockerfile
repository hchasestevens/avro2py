FROM python:3.6

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

ADD . /code
WORKDIR /code
RUN pip install -e .['dev']

VOLUME /code
