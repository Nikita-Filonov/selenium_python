from selenium.webdriver.remote.webdriver import WebElement

from utils.types.webdriver.page import PageInterface
from utils.types.webdriver.element import ElementInterface

from utils.webdriver.driver.elements_should import ElementsShould


class Elements(list[ElementInterface]):
    """Elements API: Represents a list of DOM webelements and includes commands to work with them."""

    def __init__(
        self,
        driver: PageInterface,
        web_elements: list[WebElement],
        locator: tuple[str, str] | None
    ):
        from utils.webdriver.driver.element import Element

        self._list: list[ElementInterface] = [
            Element(driver, element, None) for element in web_elements
        ]
        self._driver = driver
        self.locator = locator
        super().__init__(self._list)

    def length(self) -> int:
        """The number of elements in the list."""
        return len(self._list)

    def is_empty(self) -> bool:
        """Checks if there are zero elements in the list."""
        return self.length() == 0

    def should(self, timeout: int = 0, ignored_exceptions: list = None) -> ElementsShould:
        """A collection of expectations for this list of elements.

        Examples:
        ```
            app_web_driver.find("option").should().not_be_empty()
        ```
        """
        if timeout:
            wait_time = timeout
        else:
            wait_time = self._driver.config.driver.wait_time
        return ElementsShould(self._driver, self, wait_time, ignored_exceptions)

    def first(self) -> "ElementInterface":
        """Gets the first element in the list.

        Raises:
            `IndexError` if the list is empty.
        """
        if self.length() > 0:
            return self._list[0]
        raise IndexError("Cannot get first() from an empty list")

    def last(self) -> "ElementInterface":
        """Gets the last element in the list.

        Raises:
            `IndexError` if the list is empty.
        """
        if self.length() > 0:
            return self._list[-1]
        raise IndexError("Cannot get last() from an empty list")
