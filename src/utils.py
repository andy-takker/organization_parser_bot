import requests

REQUEST_API_URL = "https://search-maps.yandex.ru/v1/"

def search_on_maps(
    apikey: str,
    query: str,
    ll: tuple[float, float],
    spn: tuple[float, float],
    lang: str,
    type_: str,
    skip: int = 0,
    results: int = 50,
):
    result = requests.get(
        url=REQUEST_API_URL,
        params={
            "lang": lang,
            "type": type_,
            "results": results,
            "apikey": apikey,
            "text": query,
            "skip": skip,
            "ll": ",".join(map(str, ll)),
            "spn": ",".join(map(str, spn,)),
        },
    )
    return result

def km_to_ll(km: float) -> float:
    """Transfer kilometers to radian coords"""
    pass