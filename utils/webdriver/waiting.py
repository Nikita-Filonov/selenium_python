import time
from typing import Optional, Tuple, Union

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from utils.types.webdriver.waiting import Method
from utils.webdriver.element import Element, Elements


class Waiting:
    def __init__(self, py, webdriver, timeout, ignored_exceptions: Optional[Tuple] = None):
        self._py = py
        self._webdriver = webdriver
        self._wait = WebDriverWait(
            driver=webdriver,
            timeout=timeout,
            ignored_exceptions=ignored_exceptions
        )

    def sleep(self, seconds: int):
        time.sleep(seconds)

    def until(self, method: Method, message=""):
        value = self._wait.until(method, message)

        if isinstance(value, WebElement):
            return Element(self._py, value, None)

        if isinstance(value, list):
            try:
                return Elements(self._py, value, None)
            except Exception:
                pass  # not a list of WebElement

        return value

    def until_not(self, method: Method, message=""):
        value = self._wait.until_not(method, message)

        if isinstance(value, WebElement):
            return Element(self._py, value, None)

        if isinstance(value, list):
            try:
                return Elements(self._py, value, None)
            except Exception:
                pass  # not a list of WebElement

        return value

    def build(
        self, timeout: int, use_self=False, ignored_exceptions: list = None
    ) -> Union[WebDriverWait, "Waiting"]:
        if use_self:
            return Waiting(self._py, self._webdriver, timeout, ignored_exceptions)

        return WebDriverWait(self._webdriver, timeout, ignored_exceptions=ignored_exceptions)
