from enum import Enum
from json import JSONDecodeError
from typing import Any

import httpx


class CTFDError(Exception):
    """Exception class to handle exceptions thrown for any request regarding CTFd API"""


class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"


class HTTPClient:
    def __init__(
        self,
        url: str,
        token: str,
    ) -> None:
        self.client = httpx.Client(
            base_url=url,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Token {token}",
            },
        )

    def _request(
        self,
        endpoint: str,
        method: HTTPMethod,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        try:
            response = self.client.request(
                method=method.value, url=endpoint, params=params, json=json
            )

            if not response.content:
                return None

            return response.json()
        except httpx.RequestError as request_exc:
            raise CTFDError(
                f"An error occurred while requesting {request_exc.request.url!r}:\n{request_exc!r}"
            )
        except (JSONDecodeError, TypeError) as decode_exc:
            raise CTFDError(f"The response could not be parsed:\n{decode_exc!r}")

    def get_item(self, endpoint: str, id: int) -> dict[str, Any] | None:
        return self._request(f"{endpoint}/{id}", HTTPMethod.GET)

    def get_items(self, endpoint: str) -> list[dict[str, Any]] | None:
        data = self._request(endpoint, HTTPMethod.GET)
        if not data:
            return None
        
        res = [data]

        try:
            if data["meta"]["pagination"]["pages"] > 1:
                for i in range(1, data["meta"]["pagination"]["pages"] + 1):
                    new_rq = self._request(endpoint, HTTPMethod.GET, params={"page": i})
                    if not new_rq:
                        continue

                    res.append(new_rq)
        except KeyError:
            pass

        return res
