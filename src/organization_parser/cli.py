import logging
import os
from pathlib import Path
from typing import Annotated

import typer

from .utils import get_companies_dump, save_companies_to_csv_file

DEFAULT_RADIUS_KM = 10

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def cli(
    location: Annotated[
        str, typer.Argument(help="Place Where make search (ex. `Saint-Petersburg`)")
    ],
    query: Annotated[str, typer.Argument(help="What are you looking for")],
    api_key: Annotated[
        str, typer.Option(help="API key for using Yandex Places HTTP API")
    ] = "",
    radius_km: Annotated[
        float, typer.Option(help="Search radius relative to the location")
    ] = DEFAULT_RADIUS_KM,
    output_filename: Annotated[
        Path, typer.Option(help="The path to the file to save the result")
    ] = Path("./companies.csv"),
) -> None:
    api_key = api_key or os.environ.get("YANDEX_API_KEY", "")
    if api_key == "":
        raise ValueError(
            "You need to set option `api_key` or env variable `YANDEX_API_KEY`"
            "for using Yandex Geo API"
        )
    companies = get_companies_dump(
        api_key=api_key,
        location=location,
        company_query=query,
        radius_km=radius_km,
    )
    save_companies_to_csv_file(companies=companies, output_filename=output_filename)
    logger.info("Successful found: total %d companies", len(companies))


def main():
    typer.run(cli)
