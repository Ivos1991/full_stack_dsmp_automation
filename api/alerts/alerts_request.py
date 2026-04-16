class AlertsRequest:
    def __init__(self) -> None:
        self.request_body: dict = {}

    def update_alert_request(
        self,
        *,
        status: str | None = None,
        severity: str | None = None,
        assigned_to_id: str | None = None,
    ) -> "AlertsRequest":
        self.request_body = {}
        if status is not None:
            self.request_body["status"] = status
        if severity is not None:
            self.request_body["severity"] = severity
        if assigned_to_id is not None:
            self.request_body["assignedToId"] = assigned_to_id
        return self

    def add_comment_request(self, message: str) -> "AlertsRequest":
        self.request_body = {"message": message}
        return self

    def remediate_request(self, note: str | None = None) -> "AlertsRequest":
        self.request_body = {}
        if note:
            self.request_body["note"] = note
        return self
