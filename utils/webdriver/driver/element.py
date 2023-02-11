from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebElement

from utils.types.webdriver.driver.element import ElementInterface
from utils.types.webdriver.driver.elements import ElementsInterface
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

    def click(self, force=False):
        if force:
            self._page.webdriver.execute_script(
                "arguments[0].click()",
                self.web_element
            )
        else:
            self.web_element.click()

        return self._page

    def type(self, *args) -> "Element":
        ActionChains(self._page.webdriver) \
            .move_to_element(self.web_element) \
            .send_keys(*args)\
            .perform()

        return self

    def fill(self, *args) -> "Element":
        self.web_element.send_keys(args)
        return self

    def clear(self) -> "Element":
        self.web_element.clear()
        return self

    def get_xpath(self, xpath: str, timeout: int = None) -> "Element":
        by = By.XPATH

        if timeout == 0:
            elements = self.web_element.find_element(by, xpath)
        else:
            elements = self._page.wait(timeout).until(
                lambda _: self.web_element.find_element(by, xpath),
                f"Could not find any elements with the xpath: `{xpath}`",
            )

        return Element(self._page, elements, locator=(by, xpath))

    def find_xpath(self, xpath: str, timeout: int = None) -> "ElementsInterface":
        from utils.webdriver.driver.elements import Elements

        by = By.XPATH

        try:
            if timeout == 0:
                elements = self.web_element.find_elements(by, xpath)
            else:
                elements = self._page.wait(timeout).until(
                    lambda _: self.web_element.find_elements(by, xpath),
                    f"Could not find any elements with the xpath: `{xpath}`",
                )
        except TimeoutException:
            elements = []
        return Elements(self._page, elements, locator=(by, xpath))
