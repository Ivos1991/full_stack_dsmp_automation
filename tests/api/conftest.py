import pytest


@pytest.fixture(autouse=True)
def managed_api_environment(admin_service, logger):
    logger.info("Reset API environment before test")
    admin_service.reset_environment()
    yield
    logger.info("Reset API environment after test")
    admin_service.reset_environment()
