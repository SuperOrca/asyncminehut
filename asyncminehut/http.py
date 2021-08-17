import re
from typing import Union
from aiohttp import ClientResponse, ClientSession
from .errors import APIError, Unauthorized
from .constants import API_ERROR_REGEX, BASE_URL
from .utils import is_valid_uuid


class HTTP:
    def __init__(self, session: ClientSession, auth_token: str = None, session_id: str = None) -> None:
        self.session = session
        self.headers = session.headers

        if auth_token and session_id and is_valid_uuid(auth_token) and is_valid_uuid(session_id):
            self.headers['authorization'] = auth_token
            self.headers['x-session-id'] = session_id

    async def get(self, route: str, to_json=True, **kwargs) -> Union[ClientResponse, dict]:
        """A method that gets a route on the api.

        Args:
            route (str)

        Raises:
            APIError

        Returns:
            dict
        """
        response = await self.session.get(BASE_URL + route, headers=self.headers, **kwargs)
        if response.status == 403:
            raise Unauthorized
        if response.status != 200:
            error = re.findall(API_ERROR_REGEX, (await response.text()))[0]
            raise APIError(error)
        return await response.json() if to_json else response

    async def post(self, route: str, to_json=True, **kwargs) -> Union[ClientResponse, dict]:
        """A method that posts to a route on the api.

        Args:
            route (str)

        Raises:
            APIError

        Returns:
            dict
        """
        response = await self.session.post(BASE_URL + route, headers=self.headers, **kwargs)
        if response.status == 403:
            raise Unauthorized
        if response.status != 200:
            error = re.findall(API_ERROR_REGEX, (await response.text()))[0]
            raise APIError(error)
        return await response.json() if to_json else response

    async def close(self) -> None:
        """A method that closes the session."""
        await self.session.close()


__all__ = (
    "HTTP"
)
