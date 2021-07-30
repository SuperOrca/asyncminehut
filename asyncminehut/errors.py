class ServerNotFound(BaseException):
    ...


class PluginNotFound(BaseException):
    ...


class Unauthorized(BaseException):
    ...


__all__ = (
    "ServerNotFound",
    "PluginNotFound",
    "Unauthorized"
)
