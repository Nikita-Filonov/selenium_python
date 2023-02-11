from enum import IntEnum

from page_factory.button import Button
from page_factory.editor import Editor
from page_factory.table_data import TableData
from page_factory.table_row import TableRow
from page_factory.text import Text
from page_factory.title import Title
from pages.base_page import BasePage
from utils.webdriver.client import AppWebDriver


class TrySQLPageResultColumn(IntEnum):
    CUSTOMER_ID = 1
    CUSTOMER_NAME = 2
    CONTACT_NAME = 3
    ADDRESS = 4
    CITY = 5
    POSTAL_CODE = 6
    COUNTRY = 7

    @classmethod
    def to_list(
        cls,
        exclude: list['TrySQLPageResultColumn'] | None = None
    ) -> list['TrySQLPageResultColumn']:
        safe_exclude = exclude or []
        return [column for column in cls if (column not in safe_exclude)]


class TrySQLPage(BasePage):
    def __init__(self, client: AppWebDriver) -> None:
        super().__init__(client)

        self.run_sql_button = Button(
            client, locator='//button[text()="Run SQL »"]', name="Run SQL »"
        )
        self.sql_editor = Editor(
            client,
            locator='//div[@class="CodeMirror cm-s-default CodeMirror-wrap"]',
            name="SQL editor"
        )
        self.query_result_text = Text(
            client,
            locator='//div[@id="divResultSQL"]//div',
            name="Insert result"
        )
        self.number_of_records_title = Title(
            client,
            locator='//div[@id="divResultSQL"]//div//div',
            name="Number of records"
        )
        self.result_table_row = TableRow(
            client,
            locator='//div[@id="divResultSQL"]//tbody//tr',
            name='Result table row'
        )
        self.result_table_data = TableData(
            client,
            locator='//tr/td[text()="{reference_text}"]/../td[{column}]',
            name='Result table data'
        )

    def fill_sql_editor(self, sql: str):
        self.sql_editor.should_be_visible()
        self.sql_editor.clear()
        self.sql_editor.type(sql)

    def run_sql(
        self,
        empty_result: bool = False,
        rows_affected: int | None = None
    ):
        self.run_sql_button.click()

        if rows_affected:
            self.query_result_text.should_be_visible()
            self.query_result_text.should_have_text(
                f'You have made changes to the database. Rows affected: {rows_affected}'
            )

        if empty_result:
            self.query_result_text.should_be_visible()
            self.query_result_text.should_have_text('No result.')

    def check_result_table_data(
        self,
        expected_text: str,
        reference_text: str,
        column: TrySQLPageResultColumn
    ):
        self.result_table_data.should_be_visible(
            reference_text=reference_text, column=column
        )
        self.result_table_data.should_have_text(
            expected_text, reference_text=reference_text, column=column
        )

    def check_result_table_row(
        self,
        expected_texts: list[str | int],
        reference_text: str,
        columns: list[TrySQLPageResultColumn]
    ):
        for expected_text, column in zip(expected_texts, columns):
            self.check_result_table_data(
                expected_text=expected_text,
                reference_text=reference_text,
                column=column
            )

    def check_number_of_records(self, number_of_records: int):
        self.number_of_records_title.should_be_visible()
        self.number_of_records_title.should_have_text(
            f'Number of Records: {number_of_records}'
        )

        self.result_table_row.should_have_number_of_rows(number_of_records + 1)
