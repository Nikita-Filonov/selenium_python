import pytest

from config import UIConfig
from utils.webdriver.driver.page import Page
from utils.webdriver.driver.utils import attach_screenshot


@pytest.fixture(scope='session')
def ui_config() -> UIConfig:
    return UIConfig()


@pytest.fixture(scope='function')
def page(request: pytest.FixtureRequest, ui_config: UIConfig) -> Page:
    page_client = Page(ui_config)
    page_client.wait_until_stable()
    yield page_client

    if ui_config.logging.screenshots_on:
        attach_screenshot(page_client, request.node.name)

    page_client.quit()
