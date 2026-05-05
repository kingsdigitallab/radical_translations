FROM --platform=linux/amd64 node:18-slim AS client-builder

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential git \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY ./package.json /app

RUN npm install && npm cache clean --force

COPY . /app

RUN npm run build

# Python build stage
FROM python:3.7-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential git \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # LDAP dependencies
  && apt-get install -y libldap2-dev libsasl2-dev ldap-utils \
  # cron for periodic reindexing
  && apt-get install -y cron \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

RUN addgroup --system django \
  && adduser --system --ingroup django django

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/production.txt \
  && rm -rf /requirements

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint
RUN chown django /entrypoint

COPY ./compose/production/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
RUN chown django /start
COPY --from=client-builder --chown=django:django /app /app

# Cron-based periodic reindexing
COPY ./compose/production/django/reindex.sh /app/compose/production/django/reindex.sh
RUN chmod +x /app/compose/production/django/reindex.sh

COPY ./compose/production/django/reindex-cron /etc/cron.d/reindex-cron
RUN chmod 0644 /etc/cron.d/reindex-cron
RUN touch /var/log/reindex.log

# Cron-based periodic data export
COPY ./compose/production/django/export.sh /app/compose/production/django/export.sh
RUN chmod +x /app/compose/production/django/export.sh

COPY ./compose/production/django/export-cron /etc/cron.d/export-cron
RUN chmod 0644 /etc/cron.d/export-cron
RUN touch /var/log/export.log

# Load all crontabs
RUN cat /etc/cron.d/reindex-cron /etc/cron.d/export-cron | crontab -

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
