from abc import ABC, abstractclassmethod
from utils.types.webdriver.driver.page import PageInterface
from selenium.webdriver.remote.webdriver import WebElement
from utils.types.webdriver.driver.element import ElementInterface


class ElementsInterface(ABC, list[ElementInterface]):
    @abstractclassmethod
    def __init__(
        self,
        page: PageInterface,
        web_elements: list[WebElement],
        locator: tuple[str, str] | None
    ):
        self._list: list[ElementInterface]
        self._page: PageInterface
        self.locator: tuple[str, str] | None
        super().__init__(self._list)

    @abstractclassmethod
    def length(self) -> int:
        ...

    @abstractclassmethod
    def is_empty(self) -> bool:
        ...
