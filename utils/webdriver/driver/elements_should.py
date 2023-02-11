from selenium.common.exceptions import TimeoutException

from utils.types.webdriver.driver.page import PageInterface
from utils.types.webdriver.driver.elements import ElementsInterface


class ElementsShould:
    """ElementsShould API: Commands (aka Expectations) for the current list of Elements."""

    def __init__(
        self,
        page: PageInterface,
        elements: "ElementsInterface",
        timeout: int,
        ignored_exceptions: list = None
    ):
        self._page = page
        self._elements = elements
        self._wait = page.wait(
            timeout=timeout,
            use_self=True,
            ignored_exceptions=ignored_exceptions
        )

    def have_length(self, length: int) -> bool:
        try:
            if self._elements.length() == length:
                return True

            locator = self._elements.locator
            value = self._wait.until(
                lambda drvr: len(drvr.find_elements(*locator)) == length
            )
        except TimeoutException:
            value = False

        if value:
            return True

        raise AssertionError(f"Length of elements was not equal to {length}")

    def not_be_empty(self) -> ElementsInterface:
        from utils.webdriver.driver.elements import Elements

        try:
            if not self._elements.is_empty():
                return self._elements

            locator = self._elements.locator
            value = self._wait.until(lambda drvr: drvr.find_elements(*locator))
        except TimeoutException:
            value = False

        if isinstance(value, list):
            return Elements(self._page, value, self._elements.locator)

        raise AssertionError("List of elements was empty")
