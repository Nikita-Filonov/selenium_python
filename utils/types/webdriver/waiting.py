from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Callable, Union

from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.support.wait import WebDriverWait

if TYPE_CHECKING:
    from utils.types.webdriver.page import PageInterface

WebDriverUntilMethod = Callable[[WebDriver], bool]
WebElementUntilMethod = Callable[[WebElement], bool]


class WaitingInterface(ABC):

    @abstractmethod
    def __init__(
        self,
        driver: "PageInterface",
        webdriver: WebDriver,
        timeout: int,
        ignored_exceptions: tuple | None = None
    ):
        self._driver: PageInterface
        self._webdriver: WebDriver
        self._wait: WebDriverWait

    @abstractmethod
    def until(self, method: WebDriverUntilMethod, message=""):
        ...

    @abstractmethod
    def until_not(self, method: WebDriverUntilMethod, message=""):
        ...

    @abstractmethod
    def build(
        self,
        timeout: int,
        use_self=False,
        ignored_exceptions: list = None
    ) -> Union[WebDriverWait, "WaitingInterface"]:
        ...
