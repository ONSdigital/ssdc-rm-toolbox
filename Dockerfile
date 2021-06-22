FROM python:3.9-slim

RUN pip install pipenv

COPY .bashrc_extras /tmp

RUN groupadd --gid 1000 toolbox && useradd --create-home --system --uid 1000 --gid toolbox toolbox && \
    apt-get update && \
    apt-get -yq install postgresql-client || true && \
    cat /tmp/.bashrc_extras >> /home/toolbox/.bashrc && rm /tmp/.bashrc_extras
WORKDIR /home/toolbox

ENV RABBITMQ_SERVICE_HOST rabbitmq
ENV RABBITMQ_SERVICE_PORT 5672
ENV RABBITMQ_VHOST /
ENV RABBITMQ_QUEUE SampleLoader.Case.Sample
ENV RABBITMQ_USER guest
ENV RABBITMQ_PASSWORD guest

COPY Pipfile* /home/toolbox/
RUN pipenv install --system --deploy
USER toolbox

RUN mkdir /home/toolbox/.postgresql && mkdir /home/toolbox/.postgresql-rw

COPY --chown=toolbox . /home/toolbox