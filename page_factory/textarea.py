from page_factory.input import Input


class Textarea(Input):
    @property
    def type_of(self) -> str:
        return 'textarea'
