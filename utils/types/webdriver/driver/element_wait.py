from abc import ABC, abstractmethod

from selenium.webdriver.remote.webdriver import WebElement

from utils.types.webdriver.driver.page_wait import WebElementUntilMethod


class ElementWaitInterface(ABC):
    _timeout: int
    _web_element: WebElement
    _ignored_exceptions: tuple

    @abstractmethod
    def __init__(self, web_element: WebElement, timeout: int, ignored_exceptions: tuple = None):
        ...

    @abstractmethod
    def until(self, method: WebElementUntilMethod, message=""):
        ...
