# pull official base image
FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  && apt-get install -y libpq-dev \
  && apt-get install -y default-libmysqlclient-dev \
  && apt-get install -y mariadb-client \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

ENV HOME /shortlink/

# set work directory
WORKDIR $HOME

# Requirements are installed here to ensure they will be cached.
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./apps/manage.py manage.py
COPY ./apps $HOME

RUN mkdir -p /shortlink/logs

# copy entrypoint
COPY ./compose/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
