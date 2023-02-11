from page_factory.component import Component


class Text(Component):
    @property
    def type_of(self) -> str:
        return 'text'
