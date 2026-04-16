from api.base_api import BaseApi


class AuthApi(BaseApi):
    def login(self, request_body: dict) -> dict:
        return self.execute_json(
            "post",
            "/login",
            json=request_body,
            attach_name="login-response",
        )
