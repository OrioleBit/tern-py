#!/bin/sh
set -e  # exit on first error

python -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m uvicorn order_app.web_main:app --reload --host 0.0.0.0 --port 8000

exec "$@" # pass all arguments to the command