from assertpy import assert_that
from api.auth.auth_api import AuthApi
from api.auth.auth_request import AuthRequest
from api.auth.auth_response import AuthResponse


class AuthService:
    def __init__(self, auth_api: AuthApi) -> None:
        self.auth_api = auth_api

    def login(self, username: str, password: str) -> AuthResponse:
        request_body = AuthRequest().login_request(username, password).request_body
        response_data = self.auth_api.login(request_body)
        response = AuthResponse(response_data)
        assert_that(response.token).described_as("login token should be returned").is_not_empty()
        assert_that(response.user.display_name).described_as("authenticated user display name").is_equal_to("Admin")
        self.auth_api.set_token(response.token)
        return response
