from .http import HTTPClient
from .users import Users
from .teams import Teams
from .models.inputs import UserInput
from typing import Any
from .exceptions import CreationError


class CTFDClient:
    def __init__(self, url: str, token: str) -> None:
        self.http = HTTPClient(url, token)
        self._generate_packages()

    def _generate_packages(self):
        self.users = Users(self.http)
        self.teams = Teams(self.http)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.http.client.close()
        return False


    def create_full_team(self, name: str, password: str, *members: UserInput, **kwargs: dict[str, Any]) -> None:
        """
        Generate a complete team with the given parameters and its members already attached

        Args:
            name (str): The name of the team
            password (str): The password of the team
            members (UserInput): A tuple of the users to attach to the team
            kwargs (dict[str, Any]): Additional parameters to pass to the team

        Raises:
            CreationError: The team could not be created

        Returns:
            _type_: The team created with all its informations
        """
        team = self.teams.create_team(name, password)
        if not team:
            raise CreationError("Team could not be created")

        for member in members:
            new_member = self.users.create_user(member.name, member.email, member.password)
            if not new_member:
                continue # TODO : Should we raise an error here?
            self.teams.attach_member(team.id, new_member.id)
        return self.teams.get_team(team.id)