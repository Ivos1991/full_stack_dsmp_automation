from api.base_api import BaseApi


class AdminApi(BaseApi):
    def reset_environment(self) -> dict:
        return self.execute_json("post", "/admin/reset", attach_name="reset-response")
