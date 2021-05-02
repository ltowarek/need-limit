#!/bin/sh
set -e

celery -A needlimit worker -l INFO &> $HOME/celery_worker.log &
celery -A needlimit beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler &> $HOME/celery_beat.log &

exec "$@"
