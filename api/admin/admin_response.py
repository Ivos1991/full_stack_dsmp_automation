class ResetEnvironmentResponse:
    def __init__(self, data: dict) -> None:
        self.success = data["success"]
        self.message = data["message"]
