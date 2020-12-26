#!/usr/bin/env bash

#flask db upgrade

debug=${DEBUG}

if [[ $debug == "0" ]]; then
  echo "Running in production mode."
  gunicorn --worker-class gevent -w 1 --threads 2 --bind 0.0.0.0:${APP_PORT} "app:create_app()"
else
  echo "Running in non-production mode."
  python ${APP_BASE_DIR}/main.py
fi