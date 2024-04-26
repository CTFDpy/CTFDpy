from .http import HTTPClient
from .users import Users


class CTFDClient:
    def __init__(self, url: str, token: str) -> None:
        self.http = HTTPClient(url, token)
        self._generate_packages()

    def _generate_packages(self):
        self.users = Users(self.http)
