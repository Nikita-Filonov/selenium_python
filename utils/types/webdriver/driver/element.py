from abc import ABC, abstractclassmethod, abstractproperty

from selenium.webdriver.remote.webdriver import WebElement


"""
wait(e.is_visible())
"""

class ElementInterface(ABC):
    @abstractproperty
    def webelement(self) -> WebElement:
        ...

    @abstractclassmethod
    def is_displayed(self) -> bool:
        ...

    @abstractclassmethod
    def is_enabled(self) -> bool:
        ...
