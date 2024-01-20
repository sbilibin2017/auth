from sqlalchemy.ext.asyncio import AsyncEngine as AsyncSQLAlchemyEngine

__all__ = ("db",)

db: AsyncSQLAlchemyEngine | None = None
