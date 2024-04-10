from .http import HTTPClient

from .models import User

class Users:
    def __init__(self, http: HTTPClient) -> None:
        self.http = http


    def get_user(self, id: int) -> User | None:
        user_data = self.http.get_item("users", id)
        if user_data:
            return User(**user_data)
        return None
    
    def get_users(self) -> list[User] | None:
        users_data = self.http.get_items("users")
        if users_data:
            return [User(**user_data) for user_data in users_data]
        return None