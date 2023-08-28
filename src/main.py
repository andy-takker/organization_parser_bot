"""
1. Научиться запрашивать данные с API Yandex 
2. Предоставить пользователю настройку параметров поиска
3. Научиться выгружать все страницы и считать запросы
4. Научиться находить сайты организаций, переходить по ним и искать на главной почту
5. Выгрузка в Excel данных
6*. Сохранять в SQLite базу локально
7*. Добавить pre-commit
8*. Добавить Github Actions
9*. Написать тесты на pytest
"""

import os

import requests

from src.utils import search_on_maps

REQUEST_API_KEY = os.environ.get("API_KEY")
if REQUEST_API_KEY is None:
    raise ValueError("You need to set env `API_KEY` for get access to API Yandex Maps")



REQUEST_LANG = "ru_RU"
REQUEST_MAX_RESULT = 50
REQUEST_TYPE = "biz"


def main():
    search_on_maps(
        apikey=REQUEST_API_KEY,
        query="asdfasdfafda",
        lang=REQUEST_LANG,
        results=REQUEST_MAX_RESULT,
        type_=REQUEST_TYPE,
    )

if __name__ == "__main__":
    main()