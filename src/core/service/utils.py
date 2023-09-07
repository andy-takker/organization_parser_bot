import csv
import io
import logging
import math
import uuid
from pathlib import Path
from typing import Any

from src.core.dto import Company

logger = logging.getLogger(__name__)


def save_companies_to_csv_file(companies: list[Company], output_filename: Path) -> None:
    with open(output_filename, "w+") as f:
        writer = csv.DictWriter(
            f, fieldnames=["name", "address", "email", "phone", "url"]
        )
        writer.writeheader()
        writer.writerows(map(lambda c: c.to_dict(), companies))
    logger.info("Companies was written into %s", output_filename)


def save_companies_to_buffered_csv_file(companies: list[Company]) -> bytes:
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
    writer.writerow(["name", "address", "email", "phone", "url"])
    writer.writerows(map(lambda c: c.to_row(), companies))
    return output.getvalue().encode()


def parse_companies(data: dict[str, Any]) -> list[Company]:
    companies = []
    for feature in data["features"]:
        phones = feature["properties"]["CompanyMetaData"].get("Phones")
        phone = None
        if phones:
            phone = phones[0]["formatted"]
        companies.append(
            Company(
                name=feature["properties"]["CompanyMetaData"]["name"],
                address=feature["properties"]["CompanyMetaData"]["address"],
                url=feature["properties"]["CompanyMetaData"].get("url"),
                phone=phone,
            )
        )
    return companies


def km_to_ll(km: float) -> float:
    """Transfer kilometers to radian coords"""
    return km * 180 / math.pi / 6371


def validate_api_key(api_key: str) -> bool:
    try:
        uuid.UUID(api_key)
        return True
    except ValueError:
        return False
