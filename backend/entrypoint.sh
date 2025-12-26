#!/bin/sh
set -e  # exit on first error

uvicorn order_app.web_main:app --host 0.0.0.0 --port 8000

exec "$@" # pass all arguments to the command