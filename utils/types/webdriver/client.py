from abc import ABC, abstractmethod, abstractproperty

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from config import UIConfig
from utils.types.webdriver.waiting import WaitingInterface


class AppWebDriverInterface(ABC):
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
    ) -> WebDriverWait | WaitingInterface:
        pass
