import pytest

from config import UIConfig
from utils.webdriver.client import AppWebDriver


@pytest.fixture(scope='function')
def ui_config() -> UIConfig:
    return UIConfig()


@pytest.fixture(scope='function')
def webdriver(ui_config: UIConfig) -> AppWebDriver:
    client = AppWebDriver(ui_config)
    yield client

    client.quit()
