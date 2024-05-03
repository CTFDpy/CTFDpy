import httpx
import pytest
from unittest.mock import MagicMock, patch

from ctfdpy.ctfdpy.http import HTTPClient, HTTPMethod

@pytest.mark.anyio
@patch(
    "ctfdpy.ctfdpy.http.HTTPClient._call",
    return_value=httpx.Response(200, json={"success": "true", "data": [{"id": 1, "name": "user", "email": ""}]}, request=httpx.Request("GET", "http://localhost/users"))
)
def test_request_call(mocker: MagicMock):
    http = HTTPClient("http://localhost", "token")
    response: httpx.Response
    try:
        response = http._call("users", HTTPMethod.GET)
    except httpx.RequestError:
        pytest.fail("RequestError raised")

    assert response.request.method == "GET"
    assert response.request.url == "http://localhost/users"
    assert response.status_code == 200
    assert response.json() == {"success": "true", "data": [{"id": 1, "name": "user", "email": ""}]}

@pytest.mark.anyio
@patch("ctfdpy.ctfdpy.http.HTTPClient._call")
def test_get_item(mocker: MagicMock):
    http = HTTPClient("http://localhost", "token")

    mocker.return_value = httpx.Response(
        200,
        json={"success": "true", "data": {"id": 1, "name": "user", "email": ""}},
        request=httpx.Request("GET", "http://localhost/users/1")
    )
    response = http.get_item("users", 1)

    assert response == {"id": 1, "name": "user", "email": ""}