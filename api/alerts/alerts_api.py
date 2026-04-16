from api.base_api import BaseApi


class AlertsApi(BaseApi):
    def list_alerts(self, **filters: str) -> list[dict]:
        return self.execute_json("get", "/alerts", params=filters or None)

    def get_alert(self, alert_id: str) -> dict:
        return self.execute_json("get", f"/alerts/{alert_id}")

    def update_alert(self, alert_id: str, request_body: dict) -> dict:
        return self.execute_json("patch", f"/alerts/{alert_id}", json=request_body, attach_name="updated-alert")

    def add_comment(self, alert_id: str, request_body: dict) -> dict:
        return self.execute_json(
            "post",
            f"/alerts/{alert_id}/comments",
            expected_status=201,
            json=request_body,
            attach_name="alert-comment",
        )

    def remediate_alert(self, alert_id: str, request_body: dict) -> dict:
        return self.execute_json(
            "post",
            f"/alerts/{alert_id}/remediate",
            json=request_body,
            attach_name="remediation-start",
        )
