import httpx
import pytest
from unittest.mock import MagicMock, patch

from ctfdpy.ctfdpy.http import HTTPClient
from ctfdpy.ctfdpy.users import Users

@patch("ctfdpy.ctfdpy.http.HTTPClient._call")
def test_create_user(mocker: MagicMock):
    usr_obj = Users(http=HTTPClient("http://localhost", "token"))
    try:
        usr_obj.create_user("test", "", "")
    except ValueError as _:
        pass
    else:
        pytest.fail("ValueError not raised")

    mocker.return_value = httpx.Response(
        200,
        json={"success": "true", "data": {"id": 1, "name": "user", "email": "aze.rty@gmail.com", "password": "0000"}},
        request=httpx.Request("POST", "http://localhost/users", json={"name": "user", "email": "aze.rty@gmail.com", "password": "0000"})
    )

    response = usr_obj.create_user("test", "aze.rty@gmail.com", "0000")
    assert {"name": response.name, "email": response.email, "password": response.password} == {"name": "user", "email": "aze.rty@gmail.com", "password": "0000"}