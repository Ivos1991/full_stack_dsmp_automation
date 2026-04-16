class ScanResponse:
    def __init__(self, data: dict) -> None:
        self.id = data["id"]
        self.status = data["status"]
        self.started_at = data["startedAt"]
        self.completed_at = data.get("completedAt")
        self.scanned_assets_count = data["scannedAssetsCount"]
        self.alerts_created_count = data["alertsCreatedCount"]
