from .http import HTTPClient

from .models.inputs import UserInput
from .models.data import UserData

from typing import Any

class Users:
    def __init__(self, http: HTTPClient) -> None:
        self.http = http


    def get_user(self, id: int) -> UserData | None:
        user_data = self.http.get_item("users", id)
        if user_data:
            return UserData(**user_data)
        return None

    def get_users(self) -> list[UserData] | None:
        users_data = self.http.get_items("users")
        if users_data:
            return [UserData(**user_data) for user_data in users_data]
        return None

    def create_user(self, name: str, email: str, password: str) -> UserData | None:
        data: dict[str, Any] = {}
        if None in [name, email, password] or "" in [name, email, password]:
            raise ValueError("name, email and password must be provided and not empty")
        data["name"] = name
        data["email"] = email
        data["password"] = password

        user_data = self.http.post_item("users", data)
        if user_data:
            return UserData(**user_data)
        return None

    def create_batch_users(self, *users: UserInput) -> list[UserData | None]:
        return [self.create_user(user.name, user.email, user.password) for user in users]