from aiohttp import ClientTimeout

URL_REGEX = r'(((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#%])*)'
BASE_URL = 'https://api.minehut.com'
CLIENT_TIMEOUT = ClientTimeout(15)

__all__ = (
    "URL_REGEX",
    "BASE_URL",
    "CLIENT_TIMEOUT"
)
