#!/usr/bin/env bash

flask db upgrade

debug=${DEBUG}

if [[ $debug == "0" ]]; then
  echo "Running in production mode."
  # SocketIO enforcements:
  # - "worker-class" must be geventwebsocket.gunicorn.workers.GeventWebSocketWorker
  # - "workers" must be set to 1 in order to avoid flask_session issues
  gunicorn \
    --workers 1 \
    --worker-class geventwebsocket.gunicorn.workers.GeventWebSocketWorker \
    --threads 10 \
    --bind 0.0.0.0:${APP_PORT} \
    --logger-class app.loggers.GunicornLogger \
    --log-level info \
    "app:create_app('production')"
else
  echo "Running in non-production mode."
  flask auth create-admin
  python ${APP_HOME}/main.py
fi
