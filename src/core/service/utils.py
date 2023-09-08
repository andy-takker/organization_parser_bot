import csv
import io
import logging
import math
import uuid
from pathlib import Path
from typing import Any

import pandas as pd

from src.core.dto import Company

logger = logging.getLogger(__name__)


def save_companies_to_csv_file(companies: list[Company], output_filename: Path) -> None:
    with open(output_filename, "w+") as f:
        writer = csv.DictWriter(f, fieldnames=Company.header())
        writer.writeheader()
        writer.writerows(map(lambda c: c.to_dict(), companies))
    logger.info("Companies was written into %s", output_filename)


def save_companies_to_buffered_excel_file(companies: list[Company]) -> bytes:
    output = io.BytesIO()
    data = [c.to_row() for c in companies]
    df = pd.DataFrame(data=data, columns=Company.header())
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="companies", index=False)
    return output.getvalue()


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
