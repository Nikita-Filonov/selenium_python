from enum import IntEnum

import allure

from page_factory.button import Button
from page_factory.editor import Editor
from page_factory.table_data import TableData
from page_factory.table_row import TableRow
from page_factory.text import Text
from page_factory.title import Title
from pages.base_page import BasePage
from utils.webdriver.driver.page import Page


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
    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.run_sql_button = Button(
            page, locator='//button[text()="Run SQL »"]', name="Run SQL »"
        )
        self.sql_editor = Editor(
            page,
            locator='//div[@class="CodeMirror cm-s-default CodeMirror-wrap"]',
            name="SQL editor"
        )
        self.query_result_text = Text(
            page,
            locator='//div[@id="divResultSQL"]//div',
            name="Query result"
        )
        self.number_of_records_title = Title(
            page,
            locator='//div[@id="divResultSQL"]//div//div',
            name="Number of records"
        )
        self.result_table_row = TableRow(
            page,
            locator='//div[@id="divResultSQL"]//tbody//tr',
            name='Result table row'
        )
        self.result_table_data = TableData(
            page,
            locator='//tr/td[text()="{reference_text}"]/../td[{column}]',
            name='Result table data'
        )

    @allure.step('Fill SQL editor with value "{sql}"')
    def fill_sql_editor(self, sql: str):
        self.sql_editor.should_be_visible()
        self.sql_editor.clear()
        self.sql_editor.type(sql)

    @allure.step('Running SQL script')
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

    @allure.step('Checking that result table data has text "{expected_text}" in column "{column}"')
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

    @allure.step('Checking that result table row have values "{expected_texts}"')
    def check_result_table_row(
        self,
        expected_texts: tuple[str, ...],
        reference_text: str,
        columns: list[TrySQLPageResultColumn]
    ):
        for expected_text, column in zip(expected_texts, columns):
            self.check_result_table_data(
                expected_text=expected_text,
                reference_text=reference_text,
                column=column
            )

    @allure.step('Checking that number of records in result equals to "{number_of_records}"')
    def check_number_of_records(self, number_of_records: int):
        self.number_of_records_title.should_be_visible()
        self.number_of_records_title.should_have_text(
            f'Number of Records: {number_of_records}'
        )

        self.result_table_row.should_have_number_of_rows(number_of_records + 1)
