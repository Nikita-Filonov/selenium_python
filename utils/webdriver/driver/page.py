from time import sleep

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.support.wait import WebDriverWait
from urllib3.exceptions import MaxRetryError

from config import UIConfig
from utils.types.webdriver.driver.page import PageInterface
from utils.webdriver.driver.element import Element
from utils.webdriver.driver.elements import Elements
from utils.webdriver.driver.waiting import Waiting
from utils.webdriver.factory.factory import build_from_config


class Page(PageInterface):

    def __init__(self, config: UIConfig):
        self.config = config

        self._webdriver = None
        self._wait = None

    def init_webdriver(self) -> WebDriver:
        self._webdriver = build_from_config(self.config)

        self._wait = Waiting(
            self, self._webdriver, self.config.driver.wait_time, ignored_exceptions=None
        )

        if self.config.driver.page_load_wait_time:
            self.set_page_load_timeout(self.config.driver.page_load_wait_time)

        if self.config.viewport.maximize:
            self.maximize_window()
        else:
            self.viewport(
                self.config.viewport.width,
                self.config.viewport.height,
                self.config.viewport.orientation
            )
        return self._webdriver

    @property
    def webdriver(self) -> WebDriver:
        """The current instance of Selenium's `WebDriver` API."""
        return self.init_webdriver() if self._webdriver is None else self._webdriver

    def title(self) -> str:
        return self.webdriver.title

    def url(self) -> str:
        return self.webdriver.current_url

    def visit(self, url: str) -> "Page":
        normalized_url = url if url.startswith(
            'http') else (self.config.base_url + url)

        self.webdriver.get(normalized_url)
        return self

    def reload(self) -> "Page":
        self.webdriver.refresh()
        return self

    def wait_for_alive(self) -> WebDriver:
        try:
            return self.webdriver
        except MaxRetryError:
            sleep(0.5)
            self.wait_for_alive()

    def get_xpath(self, xpath: str, timeout: int = None) -> Element:
        by = By.XPATH

        if timeout == 0:
            element = self.webdriver.find_element(by, xpath)
        else:
            element = self.wait(timeout).until(
                lambda x: x.find_element(by, xpath),
                f"Could not find an element with xpath: `{xpath}`"
            )

        return Element(self, element, locator=(by, xpath))

    def find_xpath(self, xpath: str, timeout: int = None) -> Elements:
        by = By.XPATH
        elements: list[WebElement] = []

        try:
            if timeout == 0:
                elements = self.webdriver.find_elements(by, xpath)
            else:
                elements = self.wait(timeout).until(
                    lambda x: x.find_elements(by, xpath),
                    f"Could not find an element with xpath: `{xpath}`"
                )
        except TimeoutException:
            pass

        return Elements(self, elements, locator=(by, xpath))

    def wait(
            self, timeout: int = None, use_self: bool = False, ignored_exceptions: list = None
    ) -> WebDriverWait | Waiting:
        if timeout:
            return self._wait.build(timeout, use_self, ignored_exceptions)

        return self._wait.build(self.config.driver.wait_time, use_self, ignored_exceptions)

    def quit(self):
        self.webdriver.quit()

    def screenshot(self, filename: str) -> str:
        self.webdriver.save_screenshot(filename)
        return filename

    def maximize_window(self) -> "Page":
        self.webdriver.maximize_window()
        return self

    def execute_script(self, script: str, *args) -> "Page":
        self.webdriver.execute_script(script, *args)
        return self

    def set_page_load_timeout(self, timeout: int) -> "Page":
        self.webdriver.set_page_load_timeout(timeout)
        return self

    def viewport(self, width: int, height: int, orientation: str = "portrait") -> "Page":
        if orientation == "portrait":
            self.webdriver.set_window_size(width, height)
        elif orientation == "landscape":
            self.webdriver.set_window_size(height, width)
        else:
            raise ValueError("Orientation must be `portrait` or `landscape`.")
        return self
