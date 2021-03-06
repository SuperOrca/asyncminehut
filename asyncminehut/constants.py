from aiohttp import ClientTimeout

URL_REGEX = r'(((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#%])*)'
API_ERROR_REGEX = r'<pre>(.*)</pre>'
BASE_URL = 'https://api.minehut.com'
CLIENT_TIMEOUT = ClientTimeout(30)

__all__ = (
    "URL_REGEX",
    "API_ERROR_REGEX",
    "BASE_URL",
    "CLIENT_TIMEOUT"
)
