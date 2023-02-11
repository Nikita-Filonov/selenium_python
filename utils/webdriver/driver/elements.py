from selenium.webdriver.remote.webdriver import WebElement

from utils.types.webdriver.driver.page import PageInterface
from utils.types.webdriver.driver.element import ElementInterface

from utils.webdriver.driver.elements_should import ElementsShould


class Elements(list[ElementInterface]):
    """Elements API: Represents a list of DOM webelements and includes commands to work with them."""

    def __init__(
        self,
        page: PageInterface,
        web_elements: list[WebElement],
        locator: tuple[str, str] | None
    ):
        from utils.webdriver.driver.element import Element

        self._list: list[ElementInterface] = [
            Element(page, element, None) for element in web_elements
        ]
        self._page = page
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
            wait_time = self._page.config.driver.wait_time
        return ElementsShould(self._page, self, wait_time, ignored_exceptions)
