#!/bin/sh
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:7000
exec "$@"