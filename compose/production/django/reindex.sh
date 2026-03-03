#!/bin/bash

# Load environment variables from PID 1 (the entrypoint process)
export $(cat /proc/1/environ 2>/dev/null | tr '\0' '\n' | grep -E '^(DATABASE_URL|POSTGRES_|ELASTICSEARCH_|DJANGO_|REDIS_)' | xargs)

cd /app
python manage.py search_index --populate
