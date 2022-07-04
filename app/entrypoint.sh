#!/usr/bin/env sh

PORT=9077

./manage.py collectstatic --noinput && \
./manage.py download_data

if [ "$DEV" == "True" ]; then
  ./manage.py runserver 0.0.0.0:${PORT}
else
  gunicorn app.asgi:application \
    --log-file - \
    -k uvicorn.workers.UvicornWorker \
    -w 8 \
    -b 0.0.0.0:${PORT}
fi

