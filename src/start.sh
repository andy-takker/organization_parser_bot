#! /usr/bin/env sh
set -e

alembic -c ./src/alembic.ini upgrade head

exec python ./src/bot/cli.py