# Organization Parser

## Description

Utilities and Telegram bot for parsing data from [Places API](https://yandex.ru/dev/geosearch/doc/en/) by Yandex.

This can help you to search for companies and collect data about them on request to the Yandex database of organizations.

For using cli utils and bot you need to get API key from [here](https://developer.tech.yandex.com/).

(Remember that the free key allows you to make up to 500 calls to the Yandex API per day.)

<a href="https://github.com/Ileriayo/markdown-badges">
  <p align="center">
    <img alt="Python" src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"/>
    <img alt="Docker" src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white"/>
    <img alt="SQLite" src="https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white" />
    <img alt="GitHub" src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"/>
    <img alt="GitHub Actions" src="https://img.shields.io/badge/githubactions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white"/>
  </p>
</a>

Main technologies:

- [python 3.11](https://www.python.org/downloads/release/python-3110/)
- [poetry](https://python-poetry.org/)
- [aiogram 3.0](https://docs.aiogram.dev/en/v3.0.0/)
- [aiogram_dialog 2.0](https://aiogram-dialog.readthedocs.io/en/2.0.0/)
- [sqlalchemy 2.0](https://docs.sqlalchemy.org/en/20/)
- [alembic](https://alembic.sqlalchemy.org/en/latest/)
- [aiosqlite](tps://aiosqlite.omnilib.dev/en/stable/)
- [docker](https://www.docker.com/)

## Demo

You can try to using that bot [here](https://t.me/yandex_parser_bot).

## Installation

For running and building app you need to get source code of this repo:

```bash
git clone https://github.com/andy-takker/organization_parser
```

or you can get public docker image from Docker hub for ARM64 ([here](https://hub.docker.com/r/andytakker/organization_parser)).

## Configuration

An example of the settings is in the file `.env.dev`.

```bash
cp .env.dev .env
```

```bash
TELEGRAM_BOT_TOKEN  # Your telegram bot token. Required
SQLITE_DB_PATH      # Path to file sqlite db. Optional, default: ./bot.sqlite3
```

## Running

You can run bot in two ways: with docker or natively as is

### Docker

```bash
docker build . --tag organization_parser_bot:latest
docker run --env-file .env -it organization_parser_bot:latest
```

### Local

For local running I recommend use [venv](https://docs.python.org/3/library/venv.html) and you need to install poetry.

```bash
python -m venv .venv
source .venv/bin/activate  # for unix systems
pip install -U pip poetry 
poetry install --no-root
alembic -c ./src/alembic.ini upgrade head # create db and all tables
TELEGRAM_BOT_TOKEN=XXX PYTHONPATH=. python ./src/bot/main.py
```

### Database

Project database is SQLite with async driver - `aiosqlite`.

`alembic` is used to manage the database version.
To automatically create a new migration, run

```bash
alembic -c ./src/alembic.ini revision --autogenerate -m "New migration"
```

To update database to last actual version use

```bash
alembic -c ./src/alembic.ini upgrade head
```

## Using

1. At first, send `/start`
2. For registration in bot you need set `Yandex API Key` to use the API. The key looks in the UUID format
3. After that you can make requests:

   - set place where need search
   - set query (what you looking for)
   - set radius of searching

4. Click `next` to get parsed CSV file.
5. Finish!
