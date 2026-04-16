class AuthUserResponse:
    def __init__(self, data: dict) -> None:
        self.id = data["id"]
        self.display_name = data["displayName"]
        self.role = data["role"]


class AuthResponse:
    def __init__(self, data: dict) -> None:
        self.token = data["token"]
        self.user = AuthUserResponse(data["user"])
