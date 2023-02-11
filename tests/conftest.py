import pytest

from pages.try_sql_page import TrySQLPage
from utils.webdriver.driver.page import Page


@pytest.fixture(scope="function")
def try_sql_page(page: Page) -> TrySQLPage:
    return TrySQLPage(page=page)
