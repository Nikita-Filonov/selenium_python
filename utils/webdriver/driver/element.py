from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebElement

from utils.logger import logger
from utils.types.webdriver.driver.element import ElementInterface
from utils.types.webdriver.driver.page import PageInterface
from utils.webdriver.driver.element_should import ElementShould


class Element(ElementInterface):
    """Element API: Represents a single DOM webelement and includes the commands to work with it."""

    def __init__(
            self,
            page: PageInterface,
            web_element: WebElement,
            locator: tuple[str, str] | None
    ):
        self._page = page
        self._web_element = web_element
        self.locator = locator

    @property
    def web_element(self) -> WebElement:
        return self._web_element

    def should(self, timeout: int = 0, ignored_exceptions: list = None) -> ElementShould:
        """A collection of expectations for this element"""
        if timeout:
            wait_time = timeout
        else:
            wait_time = self._page.config.driver.wait_time

        return ElementShould(self._page, self, wait_time, ignored_exceptions)

    def click(self, force=False) -> "Element":
        """Clicks the element"""
        logger.info("Element.click() - Click this element")

        if force:
            self._page.webdriver.execute_script(
                "arguments[0].click()",
                self.web_element
            )
        else:
            self.web_element.click()

        return self

    def type(self, *args) -> "Element":
        """Simulate a user typing keys into the input"""
        logger.info(
            "Element.type() - Type keys `%s` into this element", (args,)
        )

        ActionChains(self._page.webdriver) \
            .move_to_element(self.web_element) \
            .send_keys(*args) \
            .perform()

        return self

    def fill(self, *args) -> "Element":
        """Fill input element with value"""
        logger.info(
            "Element.fill() - Fill value `%s` into this element", (args,)
        )

        self.web_element.send_keys(args)
        return self

    def clear(self) -> "Element":
        """Clears the text of the input or textarea element"""
        logger.info("Element.clear() - Clear the input of this element")

        self.web_element.clear()
        return self

    def is_displayed(self) -> bool:
        """Check that this element is displayed"""

        logger.info(
            "Element.is_displayed() - Check if this element is displayed"
        )

        return self.web_element.is_displayed()
