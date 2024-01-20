from faust import App as FaustApp

__all__ = ("broker",)


broker: FaustApp | None = None
