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