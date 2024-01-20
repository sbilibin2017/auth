#!/bin/bash

if [[ "${APP_DEBUG}" == "1" ]]
then
  echo "-----DEV-----"
  uvicorn main:app --host ${APP_HOST} --port ${APP_PORT} --reload
else
  echo "-----PROD-----"
  gunicorn main:app --reload --bind ${APP_HOST}:${APP_PORT} -k uvicorn.workers.UvicornWorker --threads ${APP_N_THREADS}
fi