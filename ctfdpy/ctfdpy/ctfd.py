from .http import HTTPClient
from .members import Members


class CTFDClient:
    def __init__(self, url: str, token: str) -> None:
        self.http = HTTPClient(url, token)
