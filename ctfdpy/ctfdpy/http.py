from enum import Enum
from json import JSONDecodeError
from typing import Any

import httpx

from httpx import Response

from .exceptions import RequestError, HTTPError, ParseRequestError


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
        """
        Generate a request with the given information and by using token and base_url
        Then returns the parsed response containing either the data or nothing

        Args:
            endpoint (str): The endpoint to request
            method (HTTPMethod): The HTTP method to use
            params (dict[str, Any] | None, optional): The URL parameters to send with the request. Defaults to None.
            json (dict[str, Any] | None, optional): The JSON data to send with the request. Defaults to None.

        Raises:
            RequestError: The httpx request could not be completed or ended with an unhandled error

        Returns:
            dict[str, Any] | None: The parsed response containing the data field if it exists
        """        
        try:
            return self._parse_ctfd_response(self.client.request(
                method=method.value, url=endpoint, params=params, json=json
            ))
        except httpx.RequestError as request_exc:
            raise RequestError(
                f"An error occurred while requesting {request_exc.request.url!r}:\n{request_exc!r}"
            )

    def _parse_ctfd_response(self, response: Response) -> dict[str, Any] | None:
        """
        Parse the httpx response and return the data field of the response if the request is successful
        If it encounters an error, it raises a CTFDError

        Args:
            response (Response): The response object received from the httpx request

        Raises:
            ParseRequestError: The response could not be parsed
            RequestError: The request could not be parsed or the error could not be identified
            HTTPError: The response contains an handled error status code

        Returns:
            dict[str, Any] | None: The data field of the response if the request is successful
        """

        if not response.content:
            return None
        
        data: dict[str, Any] | None = None
        try:
            data = response.json()
        except (JSONDecodeError, TypeError) as decode_exc:
            raise ParseRequestError(f"The response could not be parsed:\n{decode_exc!r}")

        if not data:
            return None

        if data.get("success", False):
            return data.get("data", None)

        if err := data.get("errors", None):
            raise HTTPError(err, response.status_code)
        
        if err := data.get("message", None):
            raise HTTPError(err, response.status_code)

        raise RequestError("An unknown error occurred while processing the request")


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
