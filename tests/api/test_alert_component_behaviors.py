import pytest
from assertpy import assert_that
from core.exceptions import ApiRequestError


@pytest.mark.api
@pytest.mark.component
def test_open_alert_cannot_jump_directly_to_resolved(scans_service, alerts_service):
    scan = scans_service.start_scan()
    scans_service.wait_for_completion(scan.id)
    alert = alerts_service.find_alert(statuses={"OPEN"}, auto_remediate=False)

    with pytest.raises(ApiRequestError) as exc_info:
        alerts_service.update_alert(alert.id, status="RESOLVED")

    assert_that(exc_info.value.status_code).described_as("invalid status transition response code").is_equal_to(400)
    assert_that(exc_info.value.response_text or "").described_as("invalid transition response body").contains("Invalid status transition")
