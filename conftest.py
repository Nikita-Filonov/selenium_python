import pytest

from config import UIConfig
from utils.webdriver.driver.page import Page


@pytest.fixture(scope='function')
def ui_config() -> UIConfig:
    return UIConfig()


@pytest.fixture(scope='function')
def page(ui_config: UIConfig) -> Page:
    page_client = Page(ui_config)
    yield page_client

    page_client.screenshot('./screenshots/some.png')
    page_client.quit()
