from page_factory.textarea import Textarea


class Editor(Textarea):
    @property
    def type_of(self) -> str:
        return 'editor'

    def clear(self):
        self._page.execute_script("window.editor.setValue('');")

    def type(self, value: str):
        self._page.execute_script(
            f"window.editor.setValue(arguments[0]);", value
        )
