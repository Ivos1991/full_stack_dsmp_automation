import os
from pathlib import Path
import pytest
from assertpy import assert_that

from api.admin.admin_api import AdminApi
from api.admin.admin_service import AdminService
from api.alerts.alerts_api import AlertsApi
from api.alerts.alerts_service import AlertsService
from api.auth.auth_api import AuthApi
from api.auth.auth_service import AuthService
from api.scans.scans_api import ScansApi
from api.scans.scans_service import ScansService
from config.settings import Settings
from core.core_utils.logger import configure_logging, get_logger


VALID_BROWSER_EVIDENCE_MODES = {"off", "on_failure", "always"}


def _cli_option_present(config: pytest.Config, option_name: str) -> bool:
    return option_name in config.invocation_params.args


def _browser_evidence_mode() -> str:
    mode = os.getenv("BROWSER_EVIDENCE_MODE", "on_failure").strip().lower()
    if mode not in VALID_BROWSER_EVIDENCE_MODES:
        raise pytest.UsageError(
            "BROWSER_EVIDENCE_MODE must be one of: off, on_failure, always"
        )
    return mode


def _apply_playwright_artifact_defaults(config: pytest.Config, items: list[pytest.Item]) -> None:
    mode = _browser_evidence_mode()
    has_collect_all_marker = any(item.get_closest_marker("collect_all_evidence") for item in items)
    force_always = mode == "always" or has_collect_all_marker

    if not _cli_option_present(config, "--output") and getattr(config.option, "output", None) == "test-results":
        config.option.output = str(Path(os.getenv("ARTIFACT_DIR", "artifacts")) / "playwright")

    if mode == "off":
        return

    if not _cli_option_present(config, "--screenshot") and getattr(config.option, "screenshot", None) == "off":
        config.option.screenshot = "on" if force_always else "only-on-failure"

    if not _cli_option_present(config, "--video") and getattr(config.option, "video", None) == "off":
        config.option.video = "on" if force_always else "retain-on-failure"

    if not _cli_option_present(config, "--tracing") and getattr(config.option, "tracing", None) == "off":
        config.option.tracing = "on" if force_always else "retain-on-failure"


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    _apply_playwright_artifact_defaults(config, items)


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings.from_env()


@pytest.fixture(scope="session", autouse=True)
def framework_logging(settings: Settings) -> None:
    configure_logging(settings.log_dir, settings.log_level)


@pytest.fixture(scope="session")
def logger():
    return get_logger("tests")


@pytest.fixture(scope="session")
def auth_api(settings: Settings) -> AuthApi:
    return AuthApi(settings)


@pytest.fixture(scope="session")
def auth_service(auth_api: AuthApi) -> AuthService:
    return AuthService(auth_api)


@pytest.fixture(scope="session")
def authenticated_api(auth_service: AuthService, settings: Settings):
    response = auth_service.login(settings.username, settings.password)
    assert_that(response.user.role).described_as("authenticated user role").is_equal_to("ADMIN")
    return response


@pytest.fixture(scope="session")
def admin_api(settings: Settings, authenticated_api) -> AdminApi:
    api = AdminApi(settings)
    api.set_token(authenticated_api.token)
    return api


@pytest.fixture(scope="session")
def admin_service(admin_api: AdminApi) -> AdminService:
    return AdminService(admin_api)


@pytest.fixture(scope="session")
def alerts_api(settings: Settings, authenticated_api) -> AlertsApi:
    api = AlertsApi(settings)
    api.set_token(authenticated_api.token)
    return api


@pytest.fixture(scope="session")
def alerts_service(alerts_api: AlertsApi, settings: Settings) -> AlertsService:
    return AlertsService(alerts_api, settings)


@pytest.fixture(scope="session")
def scans_api(settings: Settings, authenticated_api) -> ScansApi:
    api = ScansApi(settings)
    api.set_token(authenticated_api.token)
    return api


@pytest.fixture(scope="session")
def scans_service(scans_api: ScansApi, settings: Settings) -> ScansService:
    return ScansService(scans_api, settings)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)
