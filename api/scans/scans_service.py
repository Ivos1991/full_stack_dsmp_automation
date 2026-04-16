from assertpy import assert_that
from config.settings import Settings
from api.scans.scans_api import ScansApi
from api.scans.scans_response import ScanResponse
from core.core_utils.retry_utils import wait_until


class ScansService:
    def __init__(self, scans_api: ScansApi, settings: Settings) -> None:
        self.scans_api = scans_api
        self.settings = settings

    def start_scan(self) -> ScanResponse:
        response = ScanResponse(self.scans_api.start_scan())
        assert_that(response.status).described_as("newly started scan should be running").is_equal_to("RUNNING")
        return response

    def list_scans(self) -> list[ScanResponse]:
        return [ScanResponse(item) for item in self.scans_api.list_scans() or []]

    def get_scan(self, scan_id: str) -> ScanResponse:
        return ScanResponse(self.scans_api.get_scan(scan_id))

    def wait_for_completion(self, scan_id: str) -> ScanResponse:
        def _fetch() -> ScanResponse | None:
            scan = self.get_scan(scan_id)
            return scan if scan.status == "COMPLETED" else None

        completed_scan = wait_until(
            _fetch,
            timeout_seconds=self.settings.poll_timeout_seconds,
            interval_seconds=self.settings.poll_interval_seconds,
            description=f"scan {scan_id} to complete",
        )
        assert_that(completed_scan.alerts_created_count).described_as("completed scan should report created alerts").is_greater_than_or_equal_to(0)
        return completed_scan
