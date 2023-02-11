import allure

from page_factory.component import Component


class Input(Component):
    @property
    def type_of(self) -> str:
        return 'input'

    def type(self, value: str, **kwargs):
        with allure.step(f'Typing {self.type_of} "{self.name}" to value "{value}"'):
            element = self.get_element(**kwargs)
            element.type(value)

    def fill(self, value: str, **kwargs):
        with allure.step(f'Fill {self.type_of} "{self.name}" to value "{value}"'):
            element = self.get_element(**kwargs)
            element.fill(value)

    def clear(self, **kwargs):
        with allure.step(f'Clearing {self.type_of} "{self.name}"'):
            element = self.get_element(**kwargs)
            element.clear()
