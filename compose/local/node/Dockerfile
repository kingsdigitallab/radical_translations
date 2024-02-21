FROM --platform=linux/amd64 node:18-slim

RUN apt-get update \
    # dependencies for building Python packages
    && apt-get install -y build-essential git \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./package.json /app

RUN npm install -g npm
RUN npm install && npm cache clean --force

ENV PATH ./node_modules/.bin/:$PATH
