import allure
import pytest
from assertpy import assert_that
from ui.pages.alerts_page import AlertsPage


@pytest.mark.ui
def test_manual_remediation_alert_lifecycle(authenticated_page, settings, scans_service, alerts_service):
    with allure.step("Create alerts by running a scan through the API setup layer"):
        scan = scans_service.start_scan()
        scans_service.wait_for_completion(scan.id)
        manual_alert = alerts_service.find_alert(statuses={"OPEN"}, auto_remediate=False)

    page = authenticated_page
    alerts_page = AlertsPage(page, settings)

    with allure.step("Open the alerts page and locate the manual alert"):
        alerts_page.open()
        alerts_page.open_alert_by_policy_name(manual_alert.policy_name)

    with allure.step("Move alert to In Progress and assign Security Analyst"):
        alerts_page.drawer.change_status("In Progress")
        alerts_page.drawer.assign_to("Security Analyst")

    with allure.step("Add remediation note and start remediation"):
        alerts_page.drawer.add_remediation_note("Manual remediation started by automation")
        alerts_page.drawer.start_remediation()
        alerts_service.wait_for_status(manual_alert.id, {"REMEDIATED_WAITING_FOR_CUSTOMER"})
        alerts_page.drawer.wait_for_status("Awaiting User Verification")

    with allure.step("Resolve the alert and add the final verification comment"):
        alerts_page.drawer.change_status("Resolved")
        alerts_page.drawer.add_comment("Remediation verified successfully and issue is resolved")
        refreshed_alert = alerts_service.get_alert(manual_alert.id)
        assert_that(refreshed_alert.status).described_as("manual remediation final alert status").is_equal_to("RESOLVED")
        assert_that([comment.message for comment in refreshed_alert.comments]).described_as(
            "final verification comment should be persisted"
        ).contains("Remediation verified successfully and issue is resolved")
