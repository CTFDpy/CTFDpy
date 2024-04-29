from .http import HTTPClient

from .models.inputs import TeamInput
from .models.data import TeamData

from typing import Any

class Teams:
    def __init__(self, http: HTTPClient) -> None:
        self.http = http


    def get_team(self, id: int) -> TeamData | None:
        team_data = self.http.get_item("teams", id)
        if team_data:
            return TeamData(**team_data)
        return None

    def get_teams(self) -> list[TeamData] | None:
        teams_data = self.http.get_items("teams")
        if teams_data:
            return [TeamData(**team_data) for team_data in teams_data]
        return None

    def create_team(self, name: str, password: str) -> TeamData | None:
        data: dict[str, Any] = {}
        if None in [name, password] or "" in [name, password]:
            raise ValueError("name, email and password must be provided and not empty")
        data["name"] = name
        data["password"] = password

        team_data = self.http.post_item("teams", data)
        if team_data:
            return TeamData(**team_data)
        return None

    def create_batch_teams(self, *teams: TeamInput) -> list[TeamData | None]:
        return [self.create_team(team.name, team.password) for team in teams]

    def attach_member(self, team_id: int, user_id: int, is_captain: bool = False) -> None:
        self.http.post_item(f"teams/{team_id}/members", json={"user_id": user_id})
        if is_captain:
            self.http.patch_item("teams", team_id, json={"captain_id": user_id})