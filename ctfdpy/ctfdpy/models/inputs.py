from dataclasses import dataclass

all = [
    "UserInput",
]

@dataclass
class UserInput:
    name: str
    email: str
    password: str
    affiliation: str = ""
    country: str | None = None