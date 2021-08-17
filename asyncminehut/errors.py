class ServerNotFound(Exception):
    """An exception raised when the server is not found."""
    ...


class PluginNotFound(Exception):
    """An exception raised when the plugin is not found."""
    ...


class Unauthorized(Exception):
    """An exception raised when the route is unauthorized."""
    ...


class APIError(Exception):
    """An exception raised when the response from the minehut api is not 200. This could be an bug in the project."""
    ...


class InvalidCredential(Exception):
    """An exception raised when an input is invalid."""
    ...


__all__ = (
    "ServerNotFound",
    "PluginNotFound",
    "Unauthorized",
    "APIError"
)
