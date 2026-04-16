class AssigneeResponse:
    def __init__(self, data: dict) -> None:
        self.id = data["id"]
        self.name = data["name"]
        self.email = data.get("email")


class AlertCommentResponse:
    def __init__(self, data: dict) -> None:
        self.id = data["id"]
        self.author_name = data["author"]["name"]
        self.message = data["message"]
        self.created_at = data["createdAt"]


class PolicySnapshotResponse:
    def __init__(self, data: dict | None) -> None:
        self.violation_type = data.get("violationType") if data else None
        self.auto_remediate = bool(data.get("autoRemediate", False)) if data else False
        self.remediation_type = data.get("remediationType") if data else None
        self.remediation_priority = data.get("remediationPriority") if data else None
        self.remediation_due = data.get("remediationDue") if data else None
        self.supported_assets = data.get("supportedAssets") if data else None


class AlertResponse:
    def __init__(self, data: dict) -> None:
        self.id = data["id"]
        self.run_id = data["runId"]
        self.policy_id = data["policyId"]
        self.policy_name = data["policyName"]
        self.severity = data["severity"]
        self.created_severity = data.get("createdSeverity", data["severity"])
        self.status = data["status"]
        self.description = data["description"]
        self.violation_type = data["violationType"]
        self.asset_display_name = data.get("assetDisplayName") or data["asset"]["metadata"]["name"]
        self.asset_location = data.get("assetLocation") or data["asset"]["location"]
        self.was_remediated = bool(data.get("wasRemediated", False))
        self.remediation_origin = data.get("remediationOrigin", "NONE")
        self.assigned_to = AssigneeResponse(data["assignedTo"]) if data.get("assignedTo") else None
        self.comments = [AlertCommentResponse(item) for item in data.get("comments", [])]
        self.created_at = data["createdAt"]
        self.updated_at = data.get("updatedAt")
        self.valid_transitions = data.get("validTransitions", [])
        self.can_remediate = bool(data.get("canRemediate", False))
        self.policy_snapshot = PolicySnapshotResponse(data.get("policySnapshot"))

    def matches_signature(self, other: "AlertResponse") -> bool:
        return (
            self.policy_id == other.policy_id
            and self.asset_location == other.asset_location
            and self.violation_type == other.violation_type
            and self.created_severity == other.created_severity
        )
