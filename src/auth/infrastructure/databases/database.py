from contextvars import ContextVar

from sqlalchemy.ext.asyncio import AsyncEngine as AsyncSQLAlchemyEngine
from sqlalchemy.ext.asyncio import AsyncSession as AsyncSQLAlchemySession
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.auth.domain.interfaces import (IDIContainer, ILogger, ISettings,
                                        IStorageManagerWithContext,)

__all__ = (
    "DatabaseManager",
    "transaction",
)


class DatabaseManager:
    __engine: AsyncSQLAlchemyEngine
    __async_session_factory: async_sessionmaker[AsyncSQLAlchemySession]
    __ctx: ContextVar[AsyncSQLAlchemySession]

    def __init__(
        self,
        settings: ISettings,
        logger: ILogger,
    ):
        self.settings = settings
        self.logger = logger

        self.__engine = None
        self.__async_session_factory = None
        self.__ctx = None

    def get_session(self):
        session = self.__async_session_factory()
        return session

    def set_context(self):
        session: AsyncSQLAlchemySession = self.get_session()
        self.__ctx.set(session)
        return session

    def get_context(self):
        return self.__ctx.get()

    async def connect(self):
        self.__engine = create_async_engine(
            self.settings.get_db_uri(),
            echo=True,
        )
        self.__async_session_factory = async_sessionmaker(
            self.__engine, expire_on_commit=False, autoflush=False
        )
        self.__ctx = ContextVar("session", default=self.get_session())

    async def disconnect(self):
        await self.__engine.dispose()


def transaction(di_container: IDIContainer):
    db_manager = di_container.resolve(IStorageManagerWithContext)

    def wrapper(coro):
        @wraps(coro)
        async def wrapped(*args, **kwargs):
            ctx: AsyncSQLAlchemySession = db_manager.set_context()
            try:
                result = await coro(*args, **kwargs)
                await ctx.commit()
                return result
            # except DatabaseError as error:
            #     logger.error(f"Rolling back changes.\n{error}")
            #     await ctx.rollback()
            #     raise DatabaseError
            # except (IntegrityError, PendingRollbackError) as error:
            #     logger.error(f"Rolling back changes.\n{error}")
            #     await ctx.rollback()
            finally:
                await ctx.close()

        return wrapped

    return wrapper
