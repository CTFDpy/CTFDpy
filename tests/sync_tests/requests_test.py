import httpx
import pytest
from unittest.mock import MagicMock, patch

from ctfdpy.ctfdpy.http import HTTPClient, HTTPMethod
from ctfdpy.ctfdpy.exceptions import HTTPError

@pytest.mark.anyio
@patch("ctfdpy.ctfdpy.http.HTTPClient._call")
def test_request_call(mocker: MagicMock):
    http = HTTPClient("http://localhost", "token")
    response: httpx.Response

    mocker.return_value = httpx.Response(
        200,
        json={"success": "true", "data": [{"id": 1, "name": "user", "email": ""}]},
        request=httpx.Request("GET", "http://localhost/users")
    )
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
def test_parse_ctfd_response(mocker: MagicMock):
    http = HTTPClient("http://localhost", "token")

    side_effects = [
        httpx.Response(200, json={"success": "true", "data": [{"id": 1, "name": "user", "email": ""}]}, request=httpx.Request("GET", "http://localhost/users")),
        httpx.Response(400, json={"errors": "Bad Request"}, request=httpx.Request("GET", "http://localhost/users", json={"name": "user"})),
        httpx.Response(200, json={"success": "true"}, request=httpx.Request("DELETE", "http://localhost/users/1")),
        httpx.Response(200, json={}, request=httpx.Request("HEAD", "http://localhost/"))
    ]
    mocker.side_effect = side_effects
    expected_data = [
        {"id": 1, "name": "user", "email": ""},
        None,
        None,
        side_effects[-1]
    ]

    data: dict | None = {}
    try:
        data = http._parse_ctfd_response(http._call("users", HTTPMethod.GET))
    except Exception as e:
        pytest.fail(f"{type(e)} raised\n{str(e)}")
    assert data == expected_data[1]

    try:
        data = http._parse_ctfd_response(http._call("users", HTTPMethod.POST, json={"name": "user"}))
    except Exception as e:
        pytest.fail(f"{type(e)} raised\n{str(e)}")

    try:
        data = http._parse_ctfd_response(http._call("users", HTTPMethod.DELETE))
    except HTTPError as e:
        assert e.status_code == 400
        assert str(e) == f"HTTP error raised with status code {e.status_code}:\nBad Request^"
    except Exception as e2:
        pytest.fail(f"{type(e2)} raised\n{str(e2)}")
    assert data == expected_data[2]

    try:
        data = http._parse_ctfd_response(http._call("users", HTTPMethod.HEAD))
    except Exception as e:
        pytest.fail(f"{type(e)} raised\n{str(e)}")
    assert data == expected_data[3]

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