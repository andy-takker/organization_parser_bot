import os
from argparse import Namespace
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from alembic.config import Config
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

import organization_parser

PROJECT_PATH = Path(organization_parser.__file__).parent.resolve()


@asynccontextmanager
async def create_engine(
    dsn: str, debug: bool, pool_size: int, pool_timeout: int, max_overflow: int
) -> AsyncIterator[AsyncEngine]:
    engine = create_async_engine(
        url=dsn,
        echo=debug,
        pool_size=pool_size,
        pool_timeout=pool_timeout,
        max_overflow=max_overflow,
        pool_pre_ping=True,
    )
    yield engine
    await engine.dispose()


def create_sessionmaker(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )


def make_alembic_config(
    cmd_opts: Namespace,
    pg_dsn: str,
    base_path: Path = PROJECT_PATH,
) -> Config:
    if not os.path.isabs(cmd_opts.config):
        cmd_opts.config = str(base_path / "adapters/database" / cmd_opts.config)

    config = Config(
        file_=cmd_opts.config,
        ini_section=cmd_opts.name,
        cmd_opts=cmd_opts,
    )

    alembic_location = config.get_main_option("script_location")
    if not alembic_location:
        raise ValueError

    if not os.path.isabs(alembic_location):
        config.set_main_option("script_location", str(base_path / alembic_location))

    config.set_main_option("sqlalchemy.url", pg_dsn)
    config.attributes["configure_logger"] = False

    return config
