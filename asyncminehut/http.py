from typing import Dict
from .errors import APIError, Unauthorized
from .constants import BASE_URL


class HTTP:
    def __init__(self, session) -> None:
        self.session = session

    async def get(self, route: str, **kwargs) -> Dict:
        """A method that gets a route on the api.

        Args:
            route (str)

        Raises:
            APIError

        Returns:
            dict
        """
        response = await self.session.get(BASE_URL + route, **kwargs)
        if response.status == 403:
            raise Unauthorized
        if response.status != 200:
            raise APIError(f"Response returned {response.status}.")
        return await response.json()

    async def post(self, route: str, **kwargs) -> Dict:
        """A method that posts to a route on the api.

        Args:
            route (str)

        Raises:
            APIError

        Returns:
            dict
        """
        response = await self.session.post(BASE_URL + route, **kwargs)
        if response.status == 403:
            raise Unauthorized
        if response.status != 200:
            raise APIError(f"Response returned {response.status}.")
        return await response.json()

    async def close(self) -> None:
        """A method that closes the session."""
        await self.session.close()


__all__ = (
    "HTTP"
)
