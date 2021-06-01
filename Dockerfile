FROM python:3.9-slim

RUN pip install pipenv

RUN groupadd --gid 1000 toolbox && useradd --create-home --system --uid 1000 --gid toolbox toolbox
WORKDIR /home/toolbox

ENV RABBITMQ_SERVICE_HOST rabbitmq
ENV RABBITMQ_SERVICE_PORT 5672
ENV RABBITMQ_VHOST /
ENV RABBITMQ_QUEUE case.sample.inbound
ENV RABBITMQ_USER guest
ENV RABBITMQ_PASSWORD guest

COPY Pipfile* /home/toolbox/
RUN pipenv install --system --deploy
USER toolbox

COPY --chown=toolbox .. /home/toolbox