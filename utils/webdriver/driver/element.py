from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebElement

from utils.logger import logger
from utils.types.webdriver.driver.element import ElementInterface
from utils.types.webdriver.driver.page import PageInterface
from utils.webdriver.driver.element_should import ElementShould


class Element(ElementInterface):

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
        if timeout:
            wait_time = timeout
        else:
            wait_time = self._page.config.driver.wait_time

        return ElementShould(self._page, self, wait_time, ignored_exceptions)

    def click(self, force=False) -> "Element":
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
        logger.info(
            "Element.type() - Type keys `%s` into this element", (args,)
        )

        ActionChains(self._page.webdriver) \
            .move_to_element(self.web_element) \
            .send_keys(*args) \
            .perform()

        return self

    def fill(self, *args) -> "Element":
        logger.info(
            "Element.fill() - Fill value `%s` into this element", (args,)
        )

        self.web_element.send_keys(args)
        return self

    def clear(self) -> "Element":
        logger.info("Element.clear() - Clear the input of this element")

        self.web_element.clear()
        return self
