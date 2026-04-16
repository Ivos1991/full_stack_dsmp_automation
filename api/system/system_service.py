from assertpy import assert_that
from api.system.system_api import SystemApi
from api.system.system_response import HealthResponse


class SystemService:
    def __init__(self, system_api: SystemApi) -> None:
        self.system_api = system_api

    def health(self) -> HealthResponse:
        response = HealthResponse(self.system_api.health())
        assert_that(response.data).described_as("health response should not be empty").is_not_empty()
        return response

    def policy_config(self) -> dict:
        response = self.system_api.policy_config()
        assert_that(response).described_as("policy config response should not be empty").is_not_empty()
        return response
