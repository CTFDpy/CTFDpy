from dataclasses import dataclass

all = [
    "UserInput",
    "TeamInput",
]

@dataclass
class UserInput:
    name: str
    email: str
    password: str
    affiliation: str = ""
    country: str | None = None

@dataclass
class TeamInput:
    name: str
    password: str
    email: str = ""
    website: str = ""
    country: str | None = None
    bracket_id: int | None = None