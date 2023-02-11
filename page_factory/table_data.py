from page_factory.component import Component


class TableData(Component):
    @property
    def type_of(self) -> str:
        return 'table data'
