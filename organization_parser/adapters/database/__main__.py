import argparse
import logging
from pathlib import Path

from alembic.config import CommandLine

from organization_parser.adapters.database.config import DatabaseConfig
from organization_parser.adapters.database.utils import make_alembic_config

BASE_DIR = Path(__file__).resolve().parents[3]


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)

    alembic = CommandLine()
    alembic.parser.formatter_class = argparse.ArgumentDefaultsHelpFormatter

    options = alembic.parser.parse_args()
    db_config = DatabaseConfig()
    if "cmd" not in options:
        alembic.parser.error("Too few arguments")
        exit(128)
    else:
        config = make_alembic_config(cmd_opts=options, pg_dsn=db_config.dsn)
        alembic.run_cmd(config, options)
        exit()


if __name__ == "__main__":
    main()
