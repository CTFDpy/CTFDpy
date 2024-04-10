from dataclasses import dataclass

from datetime import datetime as dt

@dataclass
class User:
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
    team_id: int = 0
    created: dt| None = None