from typing import Iterable
from assertpy import assert_that
from config.settings import Settings
from api.alerts.alerts_api import AlertsApi
from api.alerts.alerts_request import AlertsRequest
from core.core_utils.retry_utils import wait_until
from api.alerts.alerts_response import AlertCommentResponse, AlertResponse


class AlertsService:
    def __init__(self, alerts_api: AlertsApi, settings: Settings) -> None:
        self.alerts_api = alerts_api
        self.settings = settings

    def list_alerts(self, **filters: str) -> list[AlertResponse]:
        return [AlertResponse(item) for item in self.alerts_api.list_alerts(**filters) or []]

    def get_alert(self, alert_id: str) -> AlertResponse:
        return AlertResponse(self.alerts_api.get_alert(alert_id))

    def update_alert(
        self,
        alert_id: str,
        *,
        status: str | None = None,
        severity: str | None = None,
        assigned_to_id: str | None = None,
    ) -> AlertResponse:
        request_body = AlertsRequest().update_alert_request(
            status=status,
            severity=severity,
            assigned_to_id=assigned_to_id,
        ).request_body
        response = AlertResponse(self.alerts_api.update_alert(alert_id, request_body))
        if status is not None:
            assert_that(response.status).described_as("updated alert status").is_equal_to(status)
        if assigned_to_id is not None:
            assert_that(response.assigned_to).described_as("updated alert assignee should exist").is_not_none()
        return response

    def add_comment(self, alert_id: str, message: str) -> AlertCommentResponse:
        request_body = AlertsRequest().add_comment_request(message).request_body
        response = AlertCommentResponse(self.alerts_api.add_comment(alert_id, request_body))
        assert_that(response.message).described_as("alert comment message").is_equal_to(message)
        return response

    def start_remediation(self, alert_id: str, note: str | None = None) -> AlertResponse:
        request_body = AlertsRequest().remediate_request(note).request_body
        response = AlertResponse(self.alerts_api.remediate_alert(alert_id, request_body))
        assert_that(response.status).described_as("alert status after remediation start").is_equal_to("REMEDIATION_IN_PROGRESS")
        return response

    def wait_for_status(self, alert_id: str, expected_statuses: Iterable[str]) -> AlertResponse:
        expected = set(expected_statuses)

        def _fetch() -> AlertResponse | None:
            alert = self.get_alert(alert_id)
            return alert if alert.status in expected else None

        response = wait_until(
            _fetch,
            timeout_seconds=self.settings.poll_timeout_seconds,
            interval_seconds=self.settings.poll_interval_seconds,
            description=f"alert {alert_id} to reach one of {sorted(expected)}",
        )
        assert_that(response.status).described_as("polled alert final status").is_in(*expected)
        return response

    def find_alert(
        self, *, statuses: Iterable[str], auto_remediate: bool) -> AlertResponse:
        allowed_statuses = set(statuses)
        candidates = self.list_alerts()
        for alert in candidates:
            if alert.status not in allowed_statuses:
                continue
            if alert.policy_snapshot.auto_remediate is auto_remediate:
                return alert
        assert_that(candidates).described_as("available alerts after scan").is_not_empty()
        raise AssertionError(
            f"No alert found for statuses={sorted(allowed_statuses)} and auto_remediate={auto_remediate}. "
            f"Available alerts={[(a.id, a.status, a.policy_snapshot.auto_remediate) for a in candidates]}"
        )
