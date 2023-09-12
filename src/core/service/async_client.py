import asyncio
from ssl import SSLError

from httpx import AsyncClient, HTTPError, Response
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
            "Occurred error. Status code: %d. message: `%s`",
            result.status_code,
            result.json()["message"],
        )
        return []
    return parse_companies(result.json())


async def preprocessed_companies(
    companies: set[Company],
) -> list[list[str]]:
    preprocessed_companies = {}
    tasks = []
    for i, company in enumerate(companies):
        preprocessed_companies[i] = company.to_row()
        tasks.append(parse_email(i, company.url))
    for i, email in await asyncio.gather(*tasks):
        preprocessed_companies[i][-1] = email
    return list(preprocessed_companies.values())


async def parse_email(company_id: int, url: str | None) -> tuple[int, str]:
    if url is None:
        return company_id, ""
    async with AsyncClient() as client:
        try:
            result = await client.get(url or "")
            return company_id, find_emails(result.text)
        except (HTTPError, SSLError) as e:
            logger.exception("Occurred exception with url={url}: {e}", url=url, e=e)
            return company_id, ""
