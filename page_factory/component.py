import allure

from utils.webdriver.client import AppWebDriver
from utils.webdriver.element import Element, Elements


class Component:
    def __init__(self, client: AppWebDriver, locator: str, name: str) -> None:
        self._client = client
        self._locator = locator
        self._name = name

    @property
    def type_of(self) -> str:
        return 'component'

    @property
    def name(self) -> str:
        return self._name

    def get_element(self, **kwargs) -> Element:
        locator = self._locator.format(**kwargs)
        return self._client.getx(locator)

    def get_elements(self, **kwargs) -> Elements:
        locator = self._locator.format(**kwargs)
        return self._client.findx(locator)

    def click(self, **kwargs) -> None:
        with allure.step(f'Clicking {self.type_of} with name "{self.name}"'):
            element = self.get_element(**kwargs)
            element.click()

    def should_be_visible(self, **kwargs) -> None:
        with allure.step(f'Checking that {self.type_of} "{self.name}" is visible'):
            element = self.get_element(**kwargs)
            element.should().be_visible()

    def should_have_text(self, text: str, **kwargs) -> None:
        with allure.step(f'Checking that {self.type_of} "{self.name}" has text "{text}"'):
            element = self.get_element(**kwargs)
            element.should().have_text(text)
