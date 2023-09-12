import asyncio

from httpx import (
    AsyncClient,
    ConnectError,
    ConnectTimeout,
    HTTPError,
    ReadError,
    Response,
)
from loguru import logger

from src.core.dto import Company
from src.core.service import REQUEST_API_URL, QueryType
from src.core.service.utils import find_emails, km_to_ll, parse_companies


async def async_search_on_maps(
    client: AsyncClient,
    query: str,
    type_: QueryType,
    ll: tuple[float, float] | None = None,
    spn: tuple[float, float] | None = None,
    skip: int = 0,
) -> Response:
    params: dict[str, int | float | str] = {
        "type": type_,
        "text": query,
        "skip": skip,
    }
    if ll is not None and spn is not None:
        params["ll"] = ",".join(map(str, ll))
        params["spn"] = ",".join(map(str, spn))
    return await client.get(REQUEST_API_URL, params=params)


async def async_get_all_results(
    client: AsyncClient, query: str, ll: tuple[float, float], radius_km: float
) -> list[list[str]]:
    radius_radian = km_to_ll(radius_km)
    spn = (radius_radian, radius_radian)

    total_companies = set()
    step = 11
    start = 0
    max_results = 50
    while True:
        tasks = [
            fast(client=client, query=query, ll=ll, spn=spn, skip=max_results * i)
            for i in range(start, start + step)
        ]
        result = await asyncio.gather(*tasks)
        f = True
        for companies in result:
            total_companies.update(companies)
            if not companies:
                f = False

        if not f:
            break
        start += step
    return await preprocessed_companies(total_companies)


async def async_get_toponym_location(
    client: AsyncClient, query: str
) -> tuple[float, ...]:
    logger.info("Search location coordinates")
    result = await async_search_on_maps(client=client, query=query, type_="geo")
    if result.status_code >= 300:
        raise ValueError(f"Result is not OK. Get status code - {result.status_code}")
    return tuple(map(float, result.json()["features"][0]["geometry"]["coordinates"]))


async def async_get_companies_dump(
    api_key: str, location: str, query: str, radius_km: float
) -> list[list[str]] | None:
    try:
        async with AsyncClient(
            params={"apikey": api_key, "lang": "ru_RU", "results": 50}
        ) as client:
            toponym_location = await async_get_toponym_location(
                client=client, query=location
            )
            return sorted(
                await async_get_all_results(
                    client=client,
                    query=query,
                    ll=toponym_location,  # type: ignore[arg-type]
                    radius_km=radius_km,
                ),
                key=lambda x: x[0],
            )
    except Exception as e:
        logger.exception(e)
        return None


async def fast(
    client: AsyncClient,
    query: str,
    ll: tuple[float, float],
    spn: tuple[float, float],
    skip: int,
) -> list[Company]:
    result = await async_search_on_maps(
        client=client,
        query=query,
        type_="biz",
        ll=ll,
        spn=spn,
        skip=skip,
    )
    if result.status_code >= 300:
        logger.error(
            "Occurred error. Status code = {code}. message = {message}",
            code=result.status_code,
            message=result.json()["message"],
        )
        return []
    return parse_companies(result.json())


async def preprocessed_companies(
    companies: set[Company],
) -> list[list[str]]:
    preprocessed_companies = []
    for company in companies:
        preprocessed_companies.append(company.to_row())
        preprocessed_companies[-1][-1] = await parse_email(company.url)
    return preprocessed_companies


async def parse_email(url: str | None) -> str:
    if url is None:
        return ""
    async with AsyncClient(
        follow_redirects=True, verify=False, timeout=10
    ) as client:  # nosec
        try:
            result = await client.get(url)
            return find_emails(result.text)
        except ConnectTimeout:
            logger.info("Occured timeout exception with url={url}", url=url)
        except ConnectError as e:
            logger.info(
                "Occurec connect error with url={url}, message={message}",
                url=url,
                message=e,
            )
        except ReadError as e:
            logger.info(
                "Occured read error with url={url}, message={message}",
                url=url,
                message=e,
            )
        except HTTPError:
            logger.exception("Occurred exception with url={url}", url=url)
        except Exception:
            pass
    return ""
