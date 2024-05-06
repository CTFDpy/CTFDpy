from .http import HTTPClient
from .users import Users
from .teams import Teams
from .models.inputs import UserInput
from .models.data import TeamData
from typing import Any
from .exceptions import CreationError


class CTFDClient:
    def __init__(self, url: str, token: str) -> None:
        self.http = HTTPClient(url, token)
        self._generate_packages()

    def _generate_packages(self):
        self.users = Users(self.http)
        self.teams = Teams(self.http)


    def create_full_team(
        self,
        name: str,
        password: str,
        members: list[UserInput],
        raise_errors: bool = False,
        **kwargs: dict[str, Any]
    )-> tuple[TeamData | None, list[Exception]]:
        """
        Generate a complete team with the given parameters and its members already attached

        Args:
            name (str): The name of the team
            password (str): The password of the team
            members (UserInput): A tuple of the users to attach to the team
            raise_errors (bool, optional): Defines if ctfdpy should raise errors (If false will skip and returns them). Defaults to False.
            kwargs (dict[str, Any]): Additional parameters to pass to the team

        Raises:
            CreationError: The team could not be created

        Returns:
            tuple[TeamData | None, list[Exception]]: The full data of the created team and the list of all errors catched during the process (only if raise_errors is set to False)
        """
        team = self.teams.create_team(name, password)
        if not team:
            raise CreationError("No entity got returned", "team", name)

        errors: list[Exception] = []
        for member in members:
            try:
                new_member = self.users.create_user(member.name, member.email, member.password)
                if not new_member:
                    error = CreationError("No entity got returned", "user", member.name)
                    if raise_errors:
                        raise error
                    errors.append(error)
                    continue

                self.teams.attach_member(team.id, new_member.id)
            except Exception as e:
                if raise_errors:
                    raise e
                errors.append(e)

        return self.teams.get_team(team.id), errors