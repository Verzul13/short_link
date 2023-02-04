# pull official base image
FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # git
  # && apt-get install -y git \
  # && apt-get install -y gettext \
  # && default-libmysqlclient-dev \
  # && apt-get install -y mysql-client \
  && apt-get install -y default-libmysqlclient-dev \
  && apt-get install -y mariadb-client \
  # pygraphviz
#  && apt-get install -y python-pygraphviz libgraphviz-dev \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

ENV HOME /esu/

# set work directory
WORKDIR $HOME

# Requirements are installed here to ensure they will be cached.
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./apps/manage.py manage.py
# COPY ./apps/app.py app.py
# COPY ./manage.py manage.py
COPY ./apps $HOME
# COPY ./config config

RUN mkdir -p /esu/logs

# copy entrypoint
COPY ./compose/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
