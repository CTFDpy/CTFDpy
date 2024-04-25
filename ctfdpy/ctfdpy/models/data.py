from dataclasses import dataclass, field
from datetime import datetime as dt

@dataclass
class UserData:
    id: int = 0
    oauth_id: int = 0
    name: str = ""
    password: str = ""
    email: str = ""
    type: str = ""
    secret: str = ""
    website: str = ""
    affiliation: str = ""
    country: str = ""
    bracket_id: int = 0
    hidden: bool = True
    banned: bool = True
    verified: bool = True
    language: str = ""
    created: dt| None = None
    fields: list = field(default_factory=list)
    team_id: int = 0
    place: int = 0
    score: int = 0