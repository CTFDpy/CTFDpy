import httpx
import pytest
from unittest.mock import MagicMock, patch

from ctfdpy.ctfdpy.http import HTTPClient, HTTPMethod
from ctfdpy.ctfdpy.exceptions import HTTPError

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

@patch("ctfdpy.ctfdpy.http.HTTPClient._call")
def test_parse_ctfd_response(mocker: MagicMock):
    http = HTTPClient("http://localhost", "token")

    side_effects = [
        httpx.Response(200, json={"success": "true", "data": {"id": 1, "name": "user", "email": ""}}, request=httpx.Request("GET", "http://localhost/users")),
        httpx.Response(400, json={"errors": "Bad Request"}, request=httpx.Request("GET", "http://localhost/users", json={"name": "user"})),
        httpx.Response(200, json={"success": "true"}, request=httpx.Request("DELETE", "http://localhost/users/1")),
        httpx.Response(200, json={}, request=httpx.Request("HEAD", "http://localhost/")),
        httpx.Response(200, json={"meta": {"pagination": {"page": 1}}, "success": "true", "data": {"id": 1, "name": "user", "email": ""}}, request=httpx.Request("HEAD", "http://localhost/"))
    ]
    mocker.side_effect = side_effects
    expected_data = [
        {"id": 1, "name": "user", "email": ""},
        None,
        None,
        side_effects[3].headers.__dict__,
        {"meta": {"pagination": {"page": 1}}, "data": {"id": 1, "name": "user", "email": ""}},
    ]

    data: dict | None = {}
    try:
        data = http._parse_ctfd_response(http._call("users", HTTPMethod.GET))
        assert data == expected_data[0]
    except Exception as e:
        pytest.fail(f"{type(e)} raised\n{str(e)}")


    try:
        data = http._parse_ctfd_response(http._call("users", HTTPMethod.POST, json={"name": "user"}))
    except HTTPError as e:
        assert e.status_code == 400
        assert str(e) == f"HTTP error raised with status code {e.status_code}:\nBad Request"
    except Exception as e:
        pytest.fail(f"{type(e)} raised\n{str(e)}")

    try:
        data = http._parse_ctfd_response(http._call("users", HTTPMethod.DELETE))
        assert data == expected_data[2]
    except Exception as e2:
        pytest.fail(f"{type(e2)} raised\n{str(e2)}")

    try:
        data = http._parse_ctfd_response(http._call("users", HTTPMethod.HEAD))
        assert data == expected_data[3]
    except Exception as e:
        pytest.fail(f"{type(e)} raised\n{str(e)}")

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

@patch("ctfdpy.ctfdpy.http.HTTPClient._call")
def test_get_items(mocker: MagicMock):
    http = HTTPClient("http://localhost", "token")

    mocker.side_effect = [
        httpx.Response(
            200,
            json={
                "meta": {
                    "pagination": {
                        "page": 1,
                        "next": 2,
                        "prev": None,
                        "pages": 2,
                        "per_page": 1,
                        "total": 2
                    }
                },
                "success": "true",
                "data": [
                    {"id": 1, "name": "user", "email": "aze.rty@gmail.com"},
                ]},
            request=httpx.Request("GET", "http://localhost/users")
        ),
        httpx.Response(
            200,
            json={
                "meta": {
                    "pagination": {
                        "page": 2,
                        "next": None,
                        "prev": 1,
                        "pages": 2,
                        "per_page": 1,
                        "total": 2
                    }
                },
                "success": "true",
                "data": [
                    {"id": 2, "name": "user2", "email": "aze.rty2@gmail.com"},
                ]},
            request=httpx.Request("GET", "http://localhost/users?page=2")
        )
    ]

    response = http.get_items("users")
    assert response == [
        {"id": 1, "name": "user", "email": "aze.rty@gmail.com"},
        {"id": 2, "name": "user2", "email": "aze.rty2@gmail.com"}
    ]

@patch("ctfdpy.ctfdpy.http.HTTPClient._call")
def test_post_item(mocker: MagicMock):
    http = HTTPClient("http://localhost", "token")

    mocker.return_value = httpx.Response(
        200,
        json={"success": "true", "data": {"id": 1, "name": "user", "email": "aze.rty@gmail.com"}},
        request=httpx.Request("POST", "http://localhost/users", json={"name": "user"})
    )

    response = http.post_item("users", json={"name": "user", "email": "aze.rty@gmail.com"})

    assert response == {"id": 1, "name": "user", "email": "aze.rty@gmail.com"}

@patch("ctfdpy.ctfdpy.http.HTTPClient._call")
def test_patch_item(mocker: MagicMock):
    http = HTTPClient("http://localhost", "token")

    mocker.return_value = httpx.Response(
        200,
        json={"success": "true", "data": {"id": 1, "name": "user", "email": "aze.rty@gmail.com"}},
        request=httpx.Request("POST", "http://localhost/users", json={"name": "user"})
    )

    response = http.post_item("users", json={"name": "user", "email": "aze.rty@gmail.com"})

    assert response == {"id": 1, "name": "user", "email": "aze.rty@gmail.com"}