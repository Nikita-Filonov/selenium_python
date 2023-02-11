from abc import ABC, abstractmethod

from selenium.webdriver.remote.webdriver import WebElement

from utils.types.webdriver.driver.element import ElementInterface
from utils.types.webdriver.driver.page import PageInterface


class ElementsInterface(ABC):
    _list: list[ElementInterface]
    _page: PageInterface
    locator: tuple[str, str] | None

    @abstractmethod
    def __init__(
            self,
            page: PageInterface,
            web_elements: list[WebElement],
            locator: tuple[str, str] | None
    ):
        ...

    @abstractmethod
    def length(self) -> int:
        ...

    @abstractmethod
    def is_empty(self) -> bool:
        ...
