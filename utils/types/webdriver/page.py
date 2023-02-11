from abc import ABC, abstractmethod, abstractproperty
from typing import TYPE_CHECKING, Union
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from config import UIConfig


if TYPE_CHECKING:
    from utils.types.webdriver.waiting import WaitingInterface


class PageInterface(ABC):
    def __init__(self, config: UIConfig) -> None:
        super().__init__()

        self.config = config

    @abstractproperty
    def webdriver(self) -> WebDriver:
        pass

    @abstractmethod
    def wait(
        self,
        timeout: int = None,
        use_self: bool = False,
        ignored_exceptions: list = None
    ) -> Union[WebDriverWait, "WaitingInterface"]:
        pass
