from core.core_utils.logger import get_logger
from playwright.sync_api import Locator, Page, expect


class PlaywrightActions:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.logger = get_logger(self.__class__.__name__)

    def fill(self, locator: Locator, value: str, description: str) -> None:
        self.logger.info("UI fill: %s", description)
        locator.fill(value)

    def click(self, locator: Locator, description: str) -> None:
        self.logger.info("UI click: %s", description)
        locator.click()

    def expect_visible(self, locator: Locator, description: str, timeout: int = 30000) -> None:
        self.logger.info("UI expect visible: %s", description)
        expect(locator, description).to_be_visible(timeout=timeout)

    def expect_text(self, locator: Locator, text: str, description: str, timeout: int = 30000) -> None:
        self.logger.info("UI expect text: %s", description)
        expect(locator, description).to_contain_text(text, timeout=timeout)

    def select_custom_option(self, trigger: Locator, option_label: str, description: str) -> None:
        self.logger.info("UI select option: %s -> %s", description, option_label)
        trigger.click()
        option = self.page.get_by_role("option", name=option_label)
        expect(option, description).to_be_visible()
        option.click()
