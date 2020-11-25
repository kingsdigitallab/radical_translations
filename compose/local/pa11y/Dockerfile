FROM alpine/git AS build_git
RUN git clone https://github.com/pa11y/pa11y-dashboard.git /app

FROM node:15-buster-slim AS build_node
COPY --from=build_git /app /app
WORKDIR /app
RUN npm install

FROM buildkite/puppeteer
COPY --from=build_node /app /app
ENV NODE_ENV=local
ADD ./compose/local/pa11y/config.json /app/config/local.json
WORKDIR /app
RUN npm install
