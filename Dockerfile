FROM python:3.9-alpine AS build-python
RUN apk update \
    && apk add gcc postgresql-dev musl-dev
COPY ./requirements.txt /
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels/ -r requirements.txt

FROM python:3.9-alpine
RUN addgroup -S app && adduser -S app -G app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apk update \
    && apk add postgresql-libs
COPY --from=build-python /wheels/ /wheels/
RUN pip install --no-cache /wheels/*
WORKDIR /code/
COPY --chown=app:app ./needlimit/ /code/
RUN python manage.py collectstatic --noinput
USER app

COPY ./docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["sh", "-c", "gunicorn needlimit.wsgi:application --bind 0.0.0.0:$PORT"]
