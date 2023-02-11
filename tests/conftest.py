import pytest

from pages.try_sql_page import TrySQLPage
from utils.webdriver.client import AppWebDriver


@pytest.fixture(scope="function")
def try_sql_page(webdriver: AppWebDriver) -> TrySQLPage:
    return TrySQLPage(client=webdriver)
