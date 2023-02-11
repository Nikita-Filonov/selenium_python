import allure

from page_factory.component import Component


class TableRow(Component):
    @property
    def type_of(self) -> str:
        return 'table row'

    def should_have_number_of_rows(self, number_of_rows: int, **kwargs):
        step_name = f'Checking that {self.type_of} with name "{self.name}" has length {number_of_rows}'
        with allure.step(step_name):
            elements = self.get_elements(**kwargs)
            elements.should().not_be_empty()
            elements.should().have_length(number_of_rows)
