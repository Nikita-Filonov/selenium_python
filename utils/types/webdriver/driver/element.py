from abc import ABC, abstractmethod

from selenium.webdriver.remote.webdriver import WebElement


class ElementInterface(ABC):
    @property
    @abstractmethod
    def web_element(self) -> WebElement:
        ...
