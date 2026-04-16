from assertpy import assert_that
from api.admin.admin_api import AdminApi
from api.admin.admin_response import ResetEnvironmentResponse


class AdminService:
    def __init__(self, admin_api: AdminApi) -> None:
        self.admin_api = admin_api

    def reset_environment(self) -> ResetEnvironmentResponse:
        response = ResetEnvironmentResponse(self.admin_api.reset_environment())
        assert_that(response.success).described_as("environment reset completed successfully").is_true()
        return response
