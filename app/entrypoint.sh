#!/usr/bin/env sh

./manage.py collectstatic --noinput && \
./manage.py download_data && \
gunicorn --reload app.asgi:application \
  --log-file - \
  -k uvicorn.workers.UvicornWorker \
  -w 8 \
  -b 0.0.0.0:8000