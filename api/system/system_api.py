from api.base_api import BaseApi


class SystemApi(BaseApi):
    def health(self) -> dict:
        return self.execute_json("get", "/health", attach_name="health")

    def policy_config(self) -> dict:
        return self.execute_json("get", "/policy-config")
