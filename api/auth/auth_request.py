class AuthRequest:
    def __init__(self) -> None:
        self.request_body: dict = {}

    def login_request(self, username: str, password: str) -> "AuthRequest":
        self.request_body = {
            "username": username,
            "password": password,
        }
        return self
