import allure
import pytest

from config import UIConfig
from utils.webdriver.driver.page import Page


@pytest.fixture(scope='function')
def ui_config() -> UIConfig:
    return UIConfig()


@pytest.fixture(scope='function')
def page(request: pytest.FixtureRequest, ui_config: UIConfig) -> Page:
    page_client = Page(ui_config)
    yield page_client

    if ui_config.logging.screenshots_on:
        screenshot = page_client.screenshot(
            f'screenshots/{request.node.name}.png'
        )
        allure.attach.file(
            screenshot, name='Page', attachment_type=allure.attachment_type.PNG
        )

    page_client.quit()
