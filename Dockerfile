# some tips from https://pythonspeed.com/articles/pipenv-docker/

FROM python:alpine

MAINTAINER Beto Fonseca <jjbeto@gmail.com>

# If MICROSERVICE is not passed as a build arg, go with evaluate
ARG MICROSERVICE=evaluate

WORKDIR /microservice

RUN set -e && \
	apk add --no-cache --virtual .build-deps \
		gcc \
		libc-dev \
		linux-headers \
    && \
    pip install --upgrade pip && \
    pip install virtualenv && \
    apk del .build-deps

# setup virtual env for all next python/pip commands
ENV VIRTUAL_ENV=/opt/venv
RUN python -m virtualenv --python=/usr/local/bin/python $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# install requirements
COPY requirements ./requirements
RUN  pip install -r ./requirements/requirements-main.txt && \
     pip install -r ./requirements/requirements-dev.txt

# Flask Port
EXPOSE 5000

ENV PYTHONPATH=/microservice
COPY ${MICROSERVICE}    ./${MICROSERVICE}
COPY shared             ./shared

COPY docker-entrypoint.sh .
RUN  chmod +x docker-entrypoint.sh
CMD  ["/microservice/docker-entrypoint.sh"]
