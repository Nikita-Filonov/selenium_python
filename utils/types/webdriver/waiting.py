from abc import ABC, abstractmethod
from typing import Any, Callable, Union

from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.support.wait import WebDriverWait

Method = Callable[[WebElement], Any]


class WaitingInterface(ABC):
    def __init__(self, py, webdriver, timeout, ignored_exceptions: tuple | None = None):
        self._py = py
        self._webdriver = webdriver
        self._wait = WebDriverWait(
            driver=webdriver,
            timeout=timeout,
            ignored_exceptions=ignored_exceptions
        )

    @abstractmethod
    def sleep(self, seconds: int):
        pass

    @abstractmethod
    def until(self, method: Method, message=""):
        pass

    @abstractmethod
    def until_not(self, method: Method, message=""):
        pass

    @abstractmethod
    def build(
        self,
        timeout: int,
        use_self=False,
        ignored_exceptions: list = None
    ) -> Union[WebDriverWait, "WaitingInterface"]:
        pass
