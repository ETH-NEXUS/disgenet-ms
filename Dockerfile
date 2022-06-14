FROM python:3.9-alpine3.13

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install --disable-pip-version-check --upgrade pip && pip install -r /requirements.txt

RUN adduser -D user
USER user

COPY ./app /app
WORKDIR /app

ENTRYPOINT [ "./entrypoint.sh" ]