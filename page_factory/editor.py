from page_factory.textarea import Textarea


class Editor(Textarea):
    @property
    def type_of(self) -> str:
        return 'editor'

    def clear(self):
        self._client.execute_script("window.editor.setValue('');")

    def type(self, value: str):
        self._client.execute_script(
            f"window.editor.setValue(arguments[0]);", value
        )
