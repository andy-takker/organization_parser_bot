from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.db.repositories.user import UserRepository


class DatabaseProvider:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user = UserRepository(session=session)
