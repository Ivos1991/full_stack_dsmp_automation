from api.base_api import BaseApi


class ScansApi(BaseApi):
    def start_scan(self) -> dict:
        return self.execute_json("post", "/scans", expected_status=201, attach_name="scan-start")

    def list_scans(self) -> list[dict]:
        return self.execute_json("get", "/scans")

    def get_scan(self, scan_id: str) -> dict:
        return self.execute_json("get", f"/scans/{scan_id}")
