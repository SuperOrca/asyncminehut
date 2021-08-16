class ServerNotFound(BaseException):
    """An exception that occurs when the server is not found."""
    ...


class PluginNotFound(BaseException):
    """An exception that occurs when the plugin is not found."""
    ...


class Unauthorized(BaseException):
    """An exception that occurs when the route is unauthorized."""
    ...

class APIError(BaseException):
    """A exception that occurs when the response from the minehut api is not 200. This could be an bug in the project."""
    ...


__all__ = (
    "ServerNotFound",
    "PluginNotFound",
    "Unauthorized",
    "APIError"
)
